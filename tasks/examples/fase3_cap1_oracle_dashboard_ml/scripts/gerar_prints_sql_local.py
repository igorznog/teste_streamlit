#!/usr/bin/env python3
"""Gera PNGs das consultas SQL a partir do CSV (mesma lógica de 03_consultas.sql).

Útil quando o Oracle ainda não está acessível: mostra que as queries foram
validadas localmente. Após rodar oracle_carga_fiap.py no servidor FIAP,
substitua por prints do SQL Developer ou pelos HTML em prints/oracle_auto/.

Uso:
    python3 scripts/gerar_prints_sql_local.py
"""

from __future__ import annotations

import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "dados" / "leituras_sensores.csv"
PRINTS = ROOT / "prints"


def load_rows() -> list[dict]:
    with CSV_PATH.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def save_table_png(name: str, title: str, headers: list[str], rows: list[list]) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("pip install matplotlib", flush=True)
        return
    PRINTS.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(min(14, 2 + len(headers) * 2), min(10, 1 + len(rows) * 0.35)))
    ax.axis("off")
    ax.set_title(f"FarmTech — {title}\n(evidência local — validar no Oracle SQL Developer)",
                 fontsize=11, pad=12)
    table = ax.table(cellText=rows, colLabels=headers, loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.2)
    dest = PRINTS / f"{name}.png"
    fig.savefig(dest, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"    ✓ {dest.name}", flush=True)


def main() -> int:
    rows = load_rows()
    for r in rows:
        r["ph"] = float(r["ph"])
        r["umidade"] = float(r["umidade"])
        r["bomba"] = int(r["bomba"])
        r["n"] = int(r["n"])
        r["p"] = int(r["p"])
        r["k"] = int(r["k"])
        dt = datetime.strptime(r["timestamp"], "%Y-%m-%d %H:%M:%S")
        r["_hora"] = dt.hour

    # Q3
    phs = [r["ph"] for r in rows]
    umids = [r["umidade"] for r in rows]
    save_table_png(
        "sql_q3_estatisticas",
        "Q3 — Estatísticas pH e umidade",
        ["métrica", "valor"],
        [
            ["ph_min", f"{min(phs):.2f}"],
            ["ph_max", f"{max(phs):.2f}"],
            ["ph_medio", f"{sum(phs)/len(phs):.2f}"],
            ["umid_min", f"{min(umids):.1f}"],
            ["umid_max", f"{max(umids):.1f}"],
            ["umid_media", f"{sum(umids)/len(umids):.1f}"],
        ],
    )

    # Q4
    bomba_on = sum(r["bomba"] for r in rows)
    total = len(rows)
    save_table_png(
        "sql_q4_bomba",
        "Q4 — Percentual bomba ligada",
        ["leituras_bomba_on", "total", "pct_bomba_on"],
        [[str(bomba_on), str(total), f"{bomba_on*100/total:.2f}"]],
    )

    # Q6
    by_h: dict[int, list[dict]] = defaultdict(list)
    for r in rows:
        by_h[r["_hora"]].append(r)
    q6_rows = []
    for h in sorted(by_h):
        grp = by_h[h]
        q6_rows.append([
            str(h),
            f"{sum(x['ph'] for x in grp)/len(grp):.2f}",
            f"{sum(x['umidade'] for x in grp)/len(grp):.1f}",
            str(len(grp)),
        ])
    save_table_png(
        "sql_q6_perfil_diario",
        "Q6 — pH e umidade médios por hora",
        ["hora", "ph_medio_hora", "umid_media_hora", "leituras"],
        q6_rows[:24],
    )

    # Q8
    q8 = [r for r in rows if r["umidade"] < 50 and r["bomba"] == 0][:20]
    save_table_png(
        "sql_q8_alertas",
        "Q8 — Solo seco com bomba desligada",
        ["timestamp", "umidade", "ph", "n", "p", "k"],
        [[r["timestamp"], str(r["umidade"]), str(r["ph"]),
          str(r["n"]), str(r["p"]), str(r["k"])] for r in q8],
    )

    # Q1 — primeiras 10
    save_table_png(
        "10_select_all",
        "Q1 — Primeiras 10 leituras (SELECT *)",
        ["timestamp", "n", "p", "k", "ph", "umidade", "bomba"],
        [[r["timestamp"], r["n"], r["p"], r["k"], str(r["ph"]),
          str(r["umidade"]), str(r["bomba"])] for r in rows[:10]],
    )

    # COUNT
    save_table_png(
        "09_count_query",
        "SELECT COUNT(*) — total importado",
        ["total_leituras"],
        [[str(total)]],
    )

    print(f"\n✓ PNGs em {PRINTS}/", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
