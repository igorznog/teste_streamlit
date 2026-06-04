#!/usr/bin/env python3
"""Gera dataset simulado de leituras de sensores da FarmTech Fase 2.

Schema (mesmo da Fase 2 — opcional2_analise/leituras_exemplo.csv):
    timestamp (ISO 8601)
    n         (0 ou 1)  — presença de nitrogênio
    p         (0 ou 1)  — presença de fósforo
    k         (0 ou 1)  — presença de potássio
    ph        (float)   — 4.0 a 9.0, café ideal 5.5–6.5
    umidade   (float %) — 30.0 a 95.0, café ideal 60–80
    bomba     (0 ou 1)  — saída da lógica de irrigação

Determinístico (seed=42) para garantir prints reproduzíveis em qualquer máquina.

Uso:
    python3 gerar_dataset.py                       # 1000 linhas em leituras_sensores.csv
    python3 gerar_dataset.py --linhas 5000 --out custom.csv
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

SCHEMA = ["timestamp", "n", "p", "k", "ph", "umidade", "bomba"]


def decidir_bomba(umidade: float, ph: float, n: int, p: int, k: int, chuva: int) -> int:
    """Mesma lógica do esp32/sketch.ino da Fase 2 (cultura: Café).

    Regras (em ordem):
      1) Chuva prevista → bomba 0.
      2) Umidade >= 80 → bomba 0 (encharcado).
      3) Umidade < 60 → bomba 1 se pH ∈ [5.0,7.0] e ≥2 de NPK presentes.
      4) 60 ≤ Umidade < 70 → bomba 1 se pH ∈ [5.0,7.0] e todos NPK presentes.
      5) Caso contrário → bomba 0.
    """
    if chuva:
        return 0
    if umidade >= 80.0:
        return 0
    npk_total = n + p + k
    ph_ok = 5.0 <= ph <= 7.0
    if umidade < 60.0:
        return 1 if (ph_ok and npk_total >= 2) else 0
    if umidade < 70.0:
        return 1 if (ph_ok and npk_total == 3) else 0
    return 0


def gerar(linhas: int, seed: int = 42, inicio: datetime | None = None,
          intervalo_min: int = 2) -> list[dict]:
    rng = random.Random(seed)
    if inicio is None:
        inicio = datetime(2026, 4, 22, 8, 0, 0)
    leituras: list[dict] = []
    # Estado contínuo (passeio aleatório) para parecer dados reais de sensor.
    umidade = 65.0
    ph = 6.1
    n, p, k = 1, 0, 1
    for i in range(linhas):
        ts = inicio + timedelta(minutes=intervalo_min * i)
        # variações lentas e realistas
        umidade += rng.gauss(0, 0.8)
        umidade = max(30.0, min(95.0, umidade))
        ph += rng.gauss(0, 0.05)
        ph = max(4.0, min(9.0, ph))
        # NPK trocam em "operações de campo" (1 a cada ~40 leituras)
        if rng.random() < 0.025:
            target = rng.choice(["n", "p", "k"])
            vals = {"n": n, "p": p, "k": k}
            vals[target] = 1 - vals[target]
            n, p, k = vals["n"], vals["p"], vals["k"]
        # Chuva é um sinal externo: ~5% das leituras (não vai pro CSV diretamente,
        # mas afeta a bomba)
        chuva = 1 if rng.random() < 0.05 else 0
        bomba = decidir_bomba(umidade, ph, n, p, k, chuva)
        leituras.append({
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "n": n,
            "p": p,
            "k": k,
            "ph": round(ph, 2),
            "umidade": round(umidade, 1),
            "bomba": bomba,
        })
    return leituras


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--linhas", type=int, default=1000,
                        help="Quantidade de leituras a gerar (default: 1000).")
    parser.add_argument("--seed", type=int, default=42,
                        help="Semente da RNG (default: 42 — determinístico).")
    parser.add_argument("--intervalo-min", type=int, default=2,
                        help="Minutos entre leituras (default: 2).")
    parser.add_argument("--out", type=str, default=None,
                        help="Arquivo de saída (default: leituras_sensores.csv ao lado deste script).")
    args = parser.parse_args()

    dest = Path(args.out) if args.out else Path(__file__).parent / "leituras_sensores.csv"
    leituras = gerar(args.linhas, seed=args.seed, intervalo_min=args.intervalo_min)
    with dest.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=SCHEMA)
        writer.writeheader()
        writer.writerows(leituras)
    bomba_on = sum(1 for r in leituras if r["bomba"] == 1)
    print(f"✓ {len(leituras)} leituras gravadas em {dest}")
    print(f"  - bomba ligada em {bomba_on} leituras ({bomba_on*100/len(leituras):.1f}%)")
    print(f"  - intervalo: {leituras[0]['timestamp']} → {leituras[-1]['timestamp']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
