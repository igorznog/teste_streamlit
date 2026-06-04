#!/bin/bash
# Sincroniza a pasta knowledge/ para uma pasta local ou do Google Drive.
#
# Configure o destino (exemplo no WSL com Google Drive for Desktop):
#   export FIAP_KNOWLEDGE_DEST="/mnt/c/Users/SEU_USUARIO/Meu Drive/FIAP_Knowledge"
# Opcional: adicione ao ~/.bashrc para persistir.
#
# Padrão se não definir: cópia em ~/FIAP_Knowledge

set -euo pipefail

DEST="${FIAP_KNOWLEDGE_DEST:-$HOME/FIAP_Knowledge}"
SRC="$(dirname "$(readlink -f "$0")")/../knowledge"

if [ ! -d "$SRC" ]; then
  echo "Erro: pasta knowledge/ não encontrada em $SRC"
  exit 1
fi

mkdir -p "$DEST"
rm -rf "${DEST:?}"/*
cp -r "$SRC"/* "$DEST"/

echo "Sync concluído: $(find "$DEST" -type f | wc -l) arquivos em $DEST"
