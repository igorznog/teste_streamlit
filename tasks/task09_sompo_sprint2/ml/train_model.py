#!/usr/bin/env python3
"""Treina o Random Forest de risco operacional do AgroKraken.

Uso:
    python ml/train_model.py
    python ml/train_model.py --csv data/dataset_simulado.csv
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dataset_simulado.csv"
MODEL_PATH = BASE_DIR / "models" / "risk_model.joblib"
METRICS_PATH = BASE_DIR / "models" / "risk_model_metrics.json"
IMPORTANCE_PATH = BASE_DIR / "models" / "feature_importance.csv"

TARGET_COLUMN = "risco_label"

NUMERIC_FEATURES = [
    "umidade_solo",
    "precipitacao_24h",
    "precipitacao_prevista",
    "temperatura",
    "declividade_terreno",
    "distancia_corpo_dagua",
    "historico_sinistros_area",
    "horas_uso_equipamento",
    "ultima_manutencao_dias",
    "velocidade_vento",
]

CATEGORICAL_FEATURES = [
    "tipo_operacao",
    "cultura",
    "tipo_solo",
]

FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES

SCORE_BANDS = {
    "baixo": {"min": 0, "max": 33},
    "medio": {"min": 34, "max": 66},
    "alto": {"min": 67, "max": 100},
}


def build_pipeline(random_state: int = 42) -> Pipeline:
    """Monta o pipeline de preprocessamento + Random Forest."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", NUMERIC_FEATURES),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                CATEGORICAL_FEATURES,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=True,
    )

    classifier = RandomForestClassifier(
        n_estimators=350,
        max_depth=8,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=random_state,
        n_jobs=-1,
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier),
        ]
    )


def load_dataset(csv_path: Path) -> pd.DataFrame:
    """Carrega e valida as colunas mínimas para treino."""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV não encontrado: {csv_path}")

    df = pd.read_csv(csv_path)
    required = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Colunas ausentes no dataset: {missing}")

    if df[TARGET_COLUMN].nunique() < 2:
        raise ValueError("O target precisa conter as classes 0 e 1.")

    return df


def feature_defaults(x_train: pd.DataFrame) -> dict[str, dict[str, Any]]:
    """Guarda valores de fallback para predicoes com campos faltantes."""
    numeric = {
        column: float(x_train[column].median())
        for column in NUMERIC_FEATURES
    }
    categorical = {}
    for column in CATEGORICAL_FEATURES:
        modes = x_train[column].mode(dropna=True)
        categorical[column] = str(modes.iloc[0]) if not modes.empty else ""

    return {"numeric": numeric, "categorical": categorical}


def feature_importance(pipeline: Pipeline) -> pd.DataFrame:
    """Extrai importancia das variaveis ja com one-hot encoding."""
    preprocessor = pipeline.named_steps["preprocessor"]
    classifier = pipeline.named_steps["classifier"]
    feature_names = preprocessor.get_feature_names_out()
    cleaned_names = [
        name.replace("num__", "").replace("cat__", "")
        for name in feature_names
    ]

    importance_df = pd.DataFrame(
        {
            "feature": cleaned_names,
            "importance": classifier.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    importance_df["importance"] = importance_df["importance"].round(6)
    return importance_df


def evaluate_model(
    pipeline: Pipeline,
    x_test: pd.DataFrame,
    y_test: pd.Series,
    threshold: float,
) -> tuple[dict[str, Any], pd.DataFrame]:
    """Calcula métricas de validação com foco em recall da classe alto risco."""
    probabilities = pipeline.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= threshold).astype(int)
    matrix = confusion_matrix(y_test, predictions, labels=[0, 1])
    tn, fp, fn, tp = matrix.ravel()
    importance_df = feature_importance(pipeline)

    metrics: dict[str, Any] = {
        "threshold": threshold,
        "classification_metrics": {
            "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
            "precision": round(float(precision_score(y_test, predictions, zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, predictions, zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_test, predictions, zero_division=0)), 4),
            "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
        },
        "confusion_matrix": {
            "labels": ["risco_baixo_0", "risco_alto_1"],
            "matrix": matrix.astype(int).tolist(),
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
            "tp": int(tp),
        },
        "classification_report": classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            target_names=["risco_baixo", "risco_alto"],
            output_dict=True,
            zero_division=0,
        ),
        "feature_importance_top10": importance_df.head(10).to_dict(orient="records"),
    }

    return metrics, importance_df


def train(
    csv_path: Path = DATA_PATH,
    model_path: Path = MODEL_PATH,
    metrics_path: Path = METRICS_PATH,
    importance_path: Path = IMPORTANCE_PATH,
    test_size: float = 0.25,
    random_state: int = 42,
    threshold: float = 0.5,
) -> dict[str, Any]:
    """Treina, valida e persiste o modelo."""
    df = load_dataset(csv_path)
    x = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].astype(int)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state,
    )

    pipeline = build_pipeline(random_state=random_state)
    pipeline.fit(x_train, y_train)

    metrics, importance_df = evaluate_model(pipeline, x_test, y_test, threshold)
    defaults = feature_defaults(x_train)

    positive_rate = float(y.mean())
    metrics.update(
        {
            "dataset": {
                "path": _display_path(csv_path),
                "rows": int(len(df)),
                "positive_label_1": int(y.sum()),
                "positive_rate": round(positive_rate, 4),
                "train_rows": int(len(x_train)),
                "test_rows": int(len(x_test)),
                "test_size": test_size,
                "random_state": random_state,
            },
            "model": {
                "algorithm": "RandomForestClassifier",
                "n_estimators": 350,
                "max_depth": 8,
                "min_samples_leaf": 2,
                "class_weight": "balanced",
            },
            "features": {
                "numeric": NUMERIC_FEATURES,
                "categorical": CATEGORICAL_FEATURES,
                "ignored": ["data_hora", "equipamento_id"],
                "target": TARGET_COLUMN,
            },
            "score_bands": SCORE_BANDS,
            "trained_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
    )

    bundle = {
        "pipeline": pipeline,
        "feature_columns": FEATURE_COLUMNS,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "target_column": TARGET_COLUMN,
        "feature_defaults": defaults,
        "threshold": threshold,
        "score_bands": SCORE_BANDS,
        "metrics": metrics["classification_metrics"],
        "trained_at_utc": metrics["trained_at_utc"],
    }

    model_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    importance_path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(bundle, model_path)
    importance_df.to_csv(importance_path, index=False, encoding="utf-8")
    with metrics_path.open("w", encoding="utf-8") as fh:
        json.dump(metrics, fh, ensure_ascii=False, indent=2)
        fh.write("\n")

    return metrics


def _display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(BASE_DIR).as_posix()
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DATA_PATH)
    parser.add_argument("--model-out", type=Path, default=MODEL_PATH)
    parser.add_argument("--metrics-out", type=Path, default=METRICS_PATH)
    parser.add_argument("--importance-out", type=Path, default=IMPORTANCE_PATH)
    parser.add_argument("--test-size", type=float, default=0.25)
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()

    metrics = train(
        csv_path=args.csv,
        model_path=args.model_out,
        metrics_path=args.metrics_out,
        importance_path=args.importance_out,
        test_size=args.test_size,
        random_state=args.random_state,
        threshold=args.threshold,
    )

    summary = metrics["classification_metrics"]
    matrix = metrics["confusion_matrix"]
    print(f"Modelo salvo em: {_display_path(args.model_out)}")
    print(f"Métricas salvas em: {_display_path(args.metrics_out)}")
    print(
        "Recall={recall:.4f} | Precision={precision:.4f} | F1={f1_score:.4f} | ROC AUC={roc_auc:.4f}".format(
            **summary
        )
    )
    print(
        "Matriz de confusão [[TN, FP], [FN, TP]] = "
        f"{matrix['matrix']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
