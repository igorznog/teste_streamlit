#!/usr/bin/env python3
"""Ingere dataset_simulado.csv no SQLite local (data/agrokraken.db).

Tabela `operacoes` — contrato com sql/01_schema.sql (Humberto).
Colunas alinhadas ao CSV de 16 campos gerado por generate_dataset.py.

Uso:
    python scripts/ingest_data.py
    python scripts/ingest_data.py --csv data/dataset_simulado.csv --db data/agrokraken.db
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path

CREATE_OPERACOES = """
CREATE TABLE IF NOT EXISTS operacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora TEXT NOT NULL,
    equipamento_id TEXT NOT NULL,
    tipo_operacao TEXT NOT NULL,
    cultura TEXT NOT NULL,
    umidade_solo REAL NOT NULL,
    precipitacao_24h REAL NOT NULL,
    precipitacao_prevista REAL NOT NULL,
    temperatura REAL NOT NULL,
    declividade_terreno REAL NOT NULL,
    distancia_corpo_dagua REAL NOT NULL,
    tipo_solo TEXT NOT NULL,
    historico_sinistros_area INTEGER NOT NULL,
    horas_uso_equipamento REAL NOT NULL,
    ultima_manutencao_dias INTEGER NOT NULL,
    velocidade_vento REAL NOT NULL,
    risco_label INTEGER NOT NULL
);
"""

CREATE_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_operacoes_equipamento ON operacoes(equipamento_id);",
    "CREATE INDEX IF NOT EXISTS idx_operacoes_risco ON operacoes(risco_label);",
    "CREATE INDEX IF NOT EXISTS idx_operacoes_data ON operacoes(data_hora);",
]

COLUMNS = [
    "data_hora", "equipamento_id", "tipo_operacao", "cultura",
    "umidade_solo", "precipitacao_24h", "precipitacao_prevista", "temperatura",
    "declividade_terreno", "distancia_corpo_dagua", "tipo_solo",
    "historico_sinistros_area", "horas_uso_equipamento", "ultima_manutencao_dias",
    "velocidade_vento", "risco_label",
]

INSERT_SQL = f"""
INSERT INTO operacoes ({", ".join(COLUMNS)})
VALUES ({", ".join("?" * len(COLUMNS))})
"""


def _parse_row(row: dict[str, str]) -> tuple:
    return (
        row["data_hora"],
        row["equipamento_id"],
        row["tipo_operacao"],
        row["cultura"],
        float(row["umidade_solo"]),
        float(row["precipitacao_24h"]),
        float(row["precipitacao_prevista"]),
        float(row["temperatura"]),
        float(row["declividade_terreno"]),
        float(row["distancia_corpo_dagua"]),
        row["tipo_solo"],
        int(row["historico_sinistros_area"]),
        float(row["horas_uso_equipamento"]),
        int(row["ultima_manutencao_dias"]),
        float(row["velocidade_vento"]),
        int(row["risco_label"]),
    )


def ingest(csv_path: Path, db_path: Path) -> int:
    """Carrega CSV e persiste na tabela operacoes."""
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV não encontrado: {csv_path}")

    with csv_path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    if not rows:
        raise ValueError("CSV vazio")

    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute("DROP TABLE IF EXISTS operacoes")
        conn.executescript(CREATE_OPERACOES)
        for idx_sql in CREATE_INDEXES:
            conn.execute(idx_sql)

        conn.executemany(INSERT_SQL, [_parse_row(r) for r in rows])
        conn.commit()

        total = conn.execute("SELECT COUNT(*) FROM operacoes").fetchone()[0]
        altos = conn.execute(
            "SELECT COUNT(*) FROM operacoes WHERE risco_label = 1"
        ).fetchone()[0]
    finally:
        conn.close()

    print(f"✓ {total} registros ingeridos em {db_path}")
    print(f"  - risco alto: {altos} ({altos * 100 / total:.1f}%)")
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    base = Path(__file__).resolve().parent.parent
    parser.add_argument("--csv", type=str, default=str(base / "data" / "dataset_simulado.csv"))
    parser.add_argument("--db", type=str, default=str(base / "data" / "agrokraken.db"))
    args = parser.parse_args()

    ingest(Path(args.csv), Path(args.db))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
