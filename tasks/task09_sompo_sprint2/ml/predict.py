#!/usr/bin/env python3
"""Predição de score de risco para consumo pelo dashboard.

Contrato com o dashboard:

    from ml.predict import predict_risk_score
    resultado = predict_risk_score(row)
"""

from __future__ import annotations

import argparse
import csv
import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_MODEL_PATH = BASE_DIR / "models" / "risk_model.joblib"
DEFAULT_CSV_PATH = BASE_DIR / "data" / "dataset_simulado.csv"


@lru_cache(maxsize=2)
def _load_bundle(model_path: str = str(DEFAULT_MODEL_PATH)) -> dict[str, Any]:
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Modelo não encontrado em {path}. Rode: python ml/train_model.py"
        )
    return joblib.load(path)


def _coerce_float(value: Any, default: float) -> float:
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _prepare_row(row: dict[str, Any], bundle: dict[str, Any]) -> pd.DataFrame:
    defaults = bundle.get("feature_defaults", {})
    numeric_defaults = defaults.get("numeric", {})
    categorical_defaults = defaults.get("categorical", {})

    prepared: dict[str, Any] = {}
    for column in bundle["numeric_features"]:
        prepared[column] = _coerce_float(
            row.get(column),
            float(numeric_defaults.get(column, 0.0)),
        )

    for column in bundle["categorical_features"]:
        fallback = categorical_defaults.get(column, "")
        value = row.get(column, fallback)
        prepared[column] = str(value if value not in (None, "") else fallback).strip().lower()

    return pd.DataFrame([prepared], columns=bundle["feature_columns"])


def _positive_probability(pipeline: Any, features: pd.DataFrame) -> float:
    probabilities = pipeline.predict_proba(features)[0]
    classes = list(getattr(pipeline, "classes_", [0, 1]))
    positive_index = classes.index(1) if 1 in classes else len(classes) - 1
    return float(probabilities[positive_index])


def _category(score: int) -> str:
    if score <= 33:
        return "baixo"
    if score <= 66:
        return "medio"
    return "alto"


def _risk_type(prepared: dict[str, Any]) -> str:
    distancia = float(prepared.get("distancia_corpo_dagua", 9999))
    umidade = float(prepared.get("umidade_solo", 0))
    precip_24h = float(prepared.get("precipitacao_24h", 0))
    precip_prev = float(prepared.get("precipitacao_prevista", 0))
    declividade = float(prepared.get("declividade_terreno", 0))
    historico = float(prepared.get("historico_sinistros_area", 0))
    manutencao = float(prepared.get("ultima_manutencao_dias", 0))
    vento = float(prepared.get("velocidade_vento", 0))
    solo = str(prepared.get("tipo_solo", "")).lower()
    operacao = str(prepared.get("tipo_operacao", "")).lower()

    if distancia < 50:
        return "proximidade crítica de corpo d'água"
    if distancia < 200:
        return "proximidade alta de corpo d'água"
    if umidade > 85 and precip_24h > 40:
        return "solo encharcado e chuva acumulada"
    if precip_24h > 40:
        return "chuva acumulada intensa"
    if precip_prev > 8:
        return "chuva prevista nas próximas horas"
    if declividade > 15:
        return "declividade elevada"
    if historico >= 3:
        return "historico recente de sinistros"
    if solo == "gleissolo":
        return "solo com alta retenção de água"
    if operacao == "transporte" and vento > 20:
        return "transporte com vento forte"
    if manutencao > 60:
        return "manutenção preventiva atrasada"
    return "operação em condições controladas"


def _recommendation(categoria: str, tipo_risco: str) -> str:
    if categoria == "alto":
        return (
            "Adiar a operação ou acionar a gestão antes de seguir; "
            f"principal fator: {tipo_risco}."
        )
    if categoria == "medio":
        return (
            "Operar com cautela, reduzir velocidade/carga e monitorar o talhão; "
            f"principal fator: {tipo_risco}."
        )
    return (
        "Operação liberada, mantendo monitoramento de rotina dos sensores e clima."
    )


def predict_risk_score(row: dict[str, Any]) -> dict[str, Any]:
    """Retorna score 0-100, categoria, tipo de risco e recomendação."""
    bundle = _load_bundle()
    features = _prepare_row(row, bundle)
    probability = _positive_probability(bundle["pipeline"], features)
    score = max(0, min(100, int(round(probability * 100))))
    categoria = _category(score)
    prepared = features.iloc[0].to_dict()
    tipo_risco = _risk_type(prepared)

    return {
        "score": score,
        "categoria": categoria,
        "tipo_risco": tipo_risco,
        "recomendacao": _recommendation(categoria, tipo_risco),
    }


def _row_from_csv(csv_path: Path, index: int) -> dict[str, Any]:
    with csv_path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise ValueError(f"CSV vazio: {csv_path}")
    if index < 0 or index >= len(rows):
        raise IndexError(f"Índice {index} fora do intervalo 0..{len(rows) - 1}")
    return rows[index]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--index", type=int, default=0)
    parser.add_argument(
        "--json-row",
        type=str,
        default=None,
        help="Linha em JSON; se informado, ignora --csv/--index.",
    )
    args = parser.parse_args()

    row = json.loads(args.json_row) if args.json_row else _row_from_csv(args.csv, args.index)
    result = predict_risk_score(row)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
