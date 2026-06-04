#!/usr/bin/env python3
"""Carga automatizada no Oracle FIAP + execução das consultas + prints HTML.

Alternativa ao wizard do SQL Developer quando você já tem acesso de rede.
Gera evidências em `prints/oracle_auto/` (HTML abrível no navegador).

Uso:
    export FIAP_ORACLE_PASSWORD='XXXXXX'   # sua data DDMMYY — NÃO commitar
    python3 scripts/oracle_carga_fiap.py

    # só testar conexão
    python3 scripts/oracle_carga_fiap.py --test-only

Requisitos:
    pip install oracledb
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "dados" / "leituras_sensores.csv"
PRINTS_DIR = ROOT / "prints" / "oracle_auto"
SQL_DIR = ROOT / "sql"

DSN = "oracle.fiap.com.br:1521/ORCL"
USER = os.environ.get("FIAP_ORACLE_USER", "RM000000")

QUERIES = {
    "q1_primeiras_10": (
        "Q1 — Primeiras 10 leituras",
        "SELECT * FROM leituras_sensores WHERE ROWNUM <= 10 ORDER BY ts",
    ),
    "q2_total": (
        "Q2 — Total de leituras",
        "SELECT COUNT(*) AS total_leituras FROM leituras_sensores",
    ),
    "q3_estatisticas": (
        "Q3 — Estatísticas pH e umidade",
        """SELECT ROUND(MIN(ph),2) AS ph_min, ROUND(MAX(ph),2) AS ph_max,
           ROUND(AVG(ph),2) AS ph_medio, ROUND(STDDEV(ph),2) AS ph_desvio,
           ROUND(MIN(umidade),1) AS umid_min, ROUND(MAX(umidade),1) AS umid_max,
           ROUND(AVG(umidade),1) AS umid_media, ROUND(STDDEV(umidade),1) AS umid_desvio
           FROM leituras_sensores""",
    ),
    "q4_bomba": (
        "Q4 — Percentual bomba ligada",
        """SELECT SUM(bomba) AS leituras_bomba_on, COUNT(*) AS total,
           ROUND(SUM(bomba)*100/COUNT(*), 2) AS pct_bomba_on
           FROM leituras_sensores""",
    ),
    "q6_perfil_diario": (
        "Q6 — pH e umidade médios por hora",
        """SELECT EXTRACT(HOUR FROM ts) AS hora,
           ROUND(AVG(ph), 2) AS ph_medio_hora,
           ROUND(AVG(umidade), 1) AS umid_media_hora,
           COUNT(*) AS leituras
           FROM leituras_sensores
           GROUP BY EXTRACT(HOUR FROM ts)
           ORDER BY hora""",
    ),
    "q8_alertas": (
        "Q8 — Solo seco com bomba desligada",
        """SELECT ts, umidade, ph, n, p, k
           FROM leituras_sensores
           WHERE umidade < 50 AND bomba = 0
           ORDER BY ts
           FETCH FIRST 20 ROWS ONLY""",
    ),
}

DDL_DROP = """
BEGIN
   EXECUTE IMMEDIATE 'DROP TABLE leituras_sensores CASCADE CONSTRAINTS';
EXCEPTION
   WHEN OTHERS THEN
      IF SQLCODE != -942 THEN RAISE; END IF;
END;
"""

DDL_CREATE = """
CREATE TABLE leituras_sensores (
   id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
   ts            TIMESTAMP        NOT NULL,
   n             NUMBER(1)        NOT NULL,
   p             NUMBER(1)        NOT NULL,
   k             NUMBER(1)        NOT NULL,
   ph            NUMBER(4,2)      NOT NULL,
   umidade       NUMBER(5,2)      NOT NULL,
   bomba         NUMBER(1)        NOT NULL
)
"""


def get_password() -> str:
    pwd = os.environ.get("FIAP_ORACLE_PASSWORD", "").strip()
    if not pwd:
        print(
            "Erro: defina FIAP_ORACLE_PASSWORD com sua senha Oracle (data DDMMYY).\n"
            "  export FIAP_ORACLE_PASSWORD='XXXXXX'",
            file=sys.stderr,
        )
        sys.exit(2)
    return pwd


def rows_to_html(title: str, sql: str, columns: list[str], rows: list[tuple]) -> str:
    thead = "".join(f"<th>{escape(c)}</th>" for c in columns)
    body_rows = []
    for row in rows[:200]:
        tds = "".join(f"<td>{escape(str(v))}</td>" for v in row)
        body_rows.append(f"<tr>{tds}</tr>")
    tbody = "\n".join(body_rows)
    if len(rows) > 200:
        tbody += f"\n<tr><td colspan='{len(columns)}'>… +{len(rows)-200} linhas</td></tr>"
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>{escape(title)}</title>
<style>
body {{ font-family: 'Segoe UI', sans-serif; margin: 24px; background: #1e1e1e; color: #eee; }}
.header {{ background: #2d2d30; padding: 12px 16px; border-left: 4px solid #e91e8c; margin-bottom: 16px; }}
.sql {{ font-family: Consolas, monospace; font-size: 12px; color: #9cdcfe; white-space: pre-wrap; }}
table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
th {{ background: #3c3c3c; padding: 8px; text-align: left; border: 1px solid #555; }}
td {{ padding: 6px 8px; border: 1px solid #444; }}
tr:nth-child(even) {{ background: #252526; }}
.meta {{ color: #888; font-size: 11px; margin-top: 8px; }}
</style></head><body>
<div class="header">
  <strong>Oracle — FIAP</strong> · {escape(title)}<br>
  <span class="meta">Usuário {escape(USER)} · {datetime.now().strftime('%d/%m/%Y %H:%M')}</span>
</div>
<pre class="sql">{escape(sql.strip())}</pre>
<table><thead><tr>{thead}</tr></thead><tbody>
{tbody}
</tbody></table>
<p class="meta">{len(rows)} linha(s) retornada(s)</p>
</body></html>"""


def save_html(name: str, html: str) -> Path:
    PRINTS_DIR.mkdir(parents=True, exist_ok=True)
    path = PRINTS_DIR / f"{name}.html"
    path.write_text(html, encoding="utf-8")
    return path


def load_csv() -> list[dict]:
    with CSV_PATH.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--test-only", action="store_true", help="Só testa SELECT FROM dual.")
    parser.add_argument("--skip-ddl", action="store_true", help="Não recria tabela (só insert se vazia).")
    args = parser.parse_args()

    try:
        import oracledb
    except ImportError:
        print("Instale: pip install oracledb", file=sys.stderr)
        return 1

    password = get_password()
    print(f"[•] Conectando {USER}@{DSN} ...", flush=True)

    with oracledb.connect(user=USER, password=password, dsn=DSN) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT USER, SYSDATE FROM dual")
            user, now = cur.fetchone()
            print(f"    ✓ Conectado: {user} @ {now}", flush=True)
            save_html(
                "00_conexao_ok",
                rows_to_html(
                    "Teste de conexão",
                    "SELECT USER, SYSDATE FROM dual",
                    ["USER", "SYSDATE"],
                    [(user, now)],
                ),
            )

            if args.test_only:
                return 0

            if not args.skip_ddl:
                print("[•] Recriando tabela leituras_sensores ...", flush=True)
                cur.execute(DDL_DROP)
                cur.execute(DDL_CREATE)
                conn.commit()

            cur.execute("SELECT COUNT(*) FROM leituras_sensores")
            count = cur.fetchone()[0]
            if count == 0:
                print("[•] Importando CSV ...", flush=True)
                rows = load_csv()
                cur.executemany(
                    """INSERT INTO leituras_sensores (ts, n, p, k, ph, umidade, bomba)
                       VALUES (TO_TIMESTAMP(:timestamp, 'YYYY-MM-DD HH24:MI:SS'),
                               :n, :p, :k, :ph, :umidade, :bomba)""",
                    rows,
                )
                conn.commit()
                print(f"    ✓ {len(rows)} linhas inseridas", flush=True)
            else:
                print(f"    Tabela já tem {count} linhas — pulando insert", flush=True)

            for key, (title, sql) in QUERIES.items():
                print(f"[•] {title} ...", flush=True)
                cur.execute(sql)
                cols = [d[0] for d in cur.description]
                data = cur.fetchall()
                path = save_html(key, rows_to_html(title, sql, cols, data))
                print(f"    ✓ {path.name} ({len(data)} linhas)", flush=True)

    print(f"\n✓ Prints HTML em {PRINTS_DIR}/", flush=True)
    print("  Abra no navegador e use Print Screen ou agent-browser screenshot.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
