#!/usr/bin/env bash
# Executa tudo da Cap 1 exceto vídeo e submissão no portal.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
  .venv/bin/pip install -q oracledb streamlit pandas plotly playwright matplotlib
  .venv/bin/playwright install chromium
fi

echo "=== 1/4 Dataset ==="
.venv/bin/python dados/gerar_dataset.py

echo "=== 2/4 Prints SQL (validação local CSV) ==="
.venv/bin/python scripts/gerar_prints_sql_local.py

echo "=== 3/4 Dashboard screenshots ==="
.venv/bin/python scripts/capture_dashboard_prints.py

echo "=== 4/4 Oracle FIAP (opcional — precisa senha) ==="
if [[ -n "${FIAP_ORACLE_PASSWORD:-}" ]]; then
  .venv/bin/python scripts/oracle_carga_fiap.py
  echo "Abra prints/oracle_auto/*.html no navegador para prints extras."
else
  echo "Pule: export FIAP_ORACLE_PASSWORD='DDMMYY' && bash scripts/run_sem_video.sh"
fi

echo ""
echo "✓ Pronto (sem vídeo). Amanhã: gravar vídeo + gh push + portal."
echo "  Ver PREPARAR_ENTREGA.md"
