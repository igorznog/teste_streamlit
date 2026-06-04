#!/usr/bin/env bash
# Setup do capturador automático do portal FIAP.
#
# Cria um virtualenv local em .venv-fiap-capture e instala Playwright + Chromium.
# Funciona em macOS, Linux e WSL2. No Linux/WSL pode pedir sudo para instalar
# bibliotecas de sistema do Chromium.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${REPO_ROOT}/.venv-fiap-capture"
REQ_FILE="${REPO_ROOT}/scripts/requirements-fiap-capture.txt"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Erro: python3 não encontrado. Instale Python 3.10+ e tente de novo." >&2
  exit 1
fi

echo "==> Criando virtualenv em ${VENV_DIR}"
python3 -m venv "${VENV_DIR}"

# shellcheck disable=SC1090,SC1091
source "${VENV_DIR}/bin/activate"

echo "==> Atualizando pip"
python -m pip install --upgrade pip >/dev/null

echo "==> Instalando dependências Python"
pip install -r "${REQ_FILE}"

echo "==> Instalando Chromium do Playwright"
python -m playwright install chromium

if [[ "$(uname -s)" == "Linux" ]]; then
  echo "==> (Linux) Tentando instalar libs de sistema do Chromium (pode pedir sudo)"
  python -m playwright install-deps chromium || echo "Aviso: install-deps falhou; veja docs/integrations/fiap-portal-capture-setup.md"
fi

cat <<EOF

Setup concluído.

Próximos passos:
  source ${VENV_DIR}/bin/activate
  python scripts/fiap_portal_capture.py login
  python scripts/fiap_portal_capture.py capture https://on.fiap.com.br/local/conteudocurso/ --slug fase3-home

EOF
