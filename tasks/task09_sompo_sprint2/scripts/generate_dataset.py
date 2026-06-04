#!/usr/bin/env python3
"""Gera dataset simulado de operações agrícolas — AgroKraken Sprint 2.

Schema alinhado ao README Sprint 1 (16 colunas).
Determinístico (seed=42) para reprodutibilidade entre integrantes.

Uso:
    python scripts/generate_dataset.py
    python scripts/generate_dataset.py --linhas 1000 --out data/dataset_simulado.csv
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

SCHEMA = [
    "data_hora",
    "equipamento_id",
    "tipo_operacao",
    "cultura",
    "umidade_solo",
    "precipitacao_24h",
    "precipitacao_prevista",
    "temperatura",
    "declividade_terreno",
    "distancia_corpo_dagua",
    "tipo_solo",
    "historico_sinistros_area",
    "horas_uso_equipamento",
    "ultima_manutencao_dias",
    "velocidade_vento",
    "risco_label",
]

EQUIPAMENTOS = [
    "TRAT-001", "TRAT-002", "TRAT-003", "TRAT-004", "TRAT-005",
    "COLH-001", "COLH-003", "COLH-005",
    "PLAN-001", "PLAN-002",
]
TIPOS_OPERACAO = ["campo", "transporte"]
CULTURAS = ["soja", "milho", "cana"]
TIPOS_SOLO = ["latossolo", "argissolo", "gleissolo"]

# Horas acumuladas por equipamento (estado entre registros)
_horas_uso: dict[str, float] = {}


def compute_risk_score(
    umidade: float,
    precip_24h: float,
    precip_prev: float,
    declividade: float,
    distancia_agua: float,
    tipo_solo: str,
    historico: int,
    tipo_operacao: str,
    manutencao_dias: int,
    vento: float,
) -> float:
    """Score interno de risco operacional (0–100) para derivar risco_label."""
    score = 0.0

    if distancia_agua < 50:
        score += 30
    elif distancia_agua < 200:
        score += 20
    elif distancia_agua < 500:
        score += 8

    if umidade > 85:
        score += 25
    elif umidade > 70:
        score += 15
    elif umidade > 60:
        score += 5

    if precip_24h > 40:
        score += 20
    elif precip_24h > 20:
        score += 10
    elif precip_24h > 5:
        score += 4

    if precip_prev > 8:
        score += 10
    elif precip_prev > 3:
        score += 5

    if declividade > 15:
        score += 15
    elif declividade > 10:
        score += 8
    elif declividade > 5:
        score += 3

    if tipo_solo == "gleissolo":
        score += 15
    elif tipo_solo == "argissolo":
        score += 8

    score += min(historico * 5, 20)

    if tipo_operacao == "transporte":
        score += 10
        if vento > 20:
            score += 8

    if manutencao_dias > 60:
        score += 10
    elif manutencao_dias > 30:
        score += 5

    return min(score, 100)


def gerar_linha(rng: random.Random, ts: datetime) -> dict:
    """Gera uma operação simulada coerente com cenários de sinistro Sompo."""
    equipamento = rng.choice(EQUIPAMENTOS)
    tipo_operacao = rng.choices(TIPOS_OPERACAO, weights=[0.75, 0.25])[0]
    cultura = rng.choice(CULTURAS)
    tipo_solo = rng.choices(TIPOS_SOLO, weights=[0.5, 0.3, 0.2])[0]

    # Gleissolo tende a ficar mais perto da água e mais úmido
    if tipo_solo == "gleissolo":
        distancia = round(rng.uniform(30, 120), 1)
        umidade = round(rng.uniform(75, 95), 1)
        precip_24h = round(rng.uniform(20, 65), 1)
    elif tipo_solo == "argissolo":
        distancia = round(rng.uniform(50, 250), 1)
        umidade = round(rng.uniform(55, 85), 1)
        precip_24h = round(rng.uniform(5, 45), 1)
    else:
        distancia = round(rng.uniform(150, 700), 1)
        umidade = round(rng.uniform(30, 70), 1)
        precip_24h = round(rng.uniform(0, 25), 1)

    precip_prev = round(rng.uniform(0, 15), 1) if precip_24h > 10 else round(rng.uniform(0, 5), 1)
    temperatura = round(rng.uniform(22, 34), 1)
    declividade = round(rng.uniform(1.5, 20), 1)
    historico = rng.randint(0, 5) if distancia < 200 else rng.randint(0, 2)
    manutencao = rng.randint(5, 95)
    vento = round(rng.uniform(4, 28), 1)

    if equipamento not in _horas_uso:
        _horas_uso[equipamento] = round(rng.uniform(150, 2000), 1)
    horas = _horas_uso[equipamento]
    _horas_uso[equipamento] = round(horas + rng.uniform(0.5, 2.0), 1)

    score = compute_risk_score(
        umidade, precip_24h, precip_prev, declividade, distancia,
        tipo_solo, historico, tipo_operacao, manutencao, vento,
    )
    risco_label = 1 if score >= 55 else 0

    return {
        "data_hora": ts.strftime("%Y-%m-%d %H:%M"),
        "equipamento_id": equipamento,
        "tipo_operacao": tipo_operacao,
        "cultura": cultura,
        "umidade_solo": umidade,
        "precipitacao_24h": precip_24h,
        "precipitacao_prevista": precip_prev,
        "temperatura": temperatura,
        "declividade_terreno": declividade,
        "distancia_corpo_dagua": distancia,
        "tipo_solo": tipo_solo,
        "historico_sinistros_area": historico,
        "horas_uso_equipamento": horas,
        "ultima_manutencao_dias": manutencao,
        "velocidade_vento": vento,
        "risco_label": risco_label,
    }


def gerar(linhas: int, seed: int = 42, inicio: datetime | None = None) -> list[dict]:
    """Gera N operações com intervalos irregulares ao longo de ~60 dias."""
    rng = random.Random(seed)
    _horas_uso.clear()
    if inicio is None:
        inicio = datetime(2026, 3, 10, 6, 0)

    registros: list[dict] = []
    ts = inicio
    for _ in range(linhas):
        hora = rng.choice([6, 7, 8, 9, 14, 15])
        minuto = rng.choice([0, 15, 30, 45])
        ts = ts.replace(hour=hora, minute=minuto)
        registros.append(gerar_linha(rng, ts))
        ts += timedelta(days=rng.randint(0, 1), hours=rng.randint(1, 4))

    return registros


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--linhas", type=int, default=600,
                        help="Quantidade de operações (default: 600).")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=str, default=None,
                        help="CSV de saída (default: data/dataset_simulado.csv).")
    args = parser.parse_args()

    base = Path(__file__).resolve().parent.parent
    dest = Path(args.out) if args.out else base / "data" / "dataset_simulado.csv"
    dest.parent.mkdir(parents=True, exist_ok=True)

    registros = gerar(args.linhas, seed=args.seed)
    with dest.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=SCHEMA)
        writer.writeheader()
        writer.writerows(registros)

    altos = sum(1 for r in registros if r["risco_label"] == 1)
    print(f"✓ {len(registros)} operações gravadas em {dest}")
    print(f"  - risco alto (label=1): {altos} ({altos * 100 / len(registros):.1f}%)")
    print(f"  - período: {registros[0]['data_hora']} → {registros[-1]['data_hora']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
