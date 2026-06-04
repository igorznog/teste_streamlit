#!/usr/bin/env bash
# Atualiza dashboards do workflow em silêncio quando as fontes mudarem.
# Fail-open por design: dashboard desatualizado não deve bloquear o agente.

set -u

ROOT="$(pwd)"
SCRIPT="$ROOT/scripts/update_workflow_dashboard.py"
REGISTRY="$ROOT/TASK_REGISTRY.md"
GROUP="$ROOT/GROUP.md"
OUT_DIR="$ROOT/docs/dashboard"

# Consome o JSON do hook sem produzir saída para o contexto do agente.
if [ ! -t 0 ]; then
  cat >/dev/null || true
fi

if [ ! -f "$SCRIPT" ] || [ ! -f "$REGISTRY" ] || [ ! -f "$GROUP" ]; then
  exit 0
fi

needs_update=false
for target in index.html grupo.html individual.html registry.html; do
  if [ ! -f "$OUT_DIR/$target" ]; then
    needs_update=true
    break
  fi
done

if [ "$needs_update" = false ]; then
  for source in "$REGISTRY" "$GROUP" "$SCRIPT"; do
    for target in "$OUT_DIR/index.html" "$OUT_DIR/grupo.html" "$OUT_DIR/individual.html" "$OUT_DIR/registry.html"; do
      if [ "$source" -nt "$target" ]; then
        needs_update=true
        break 2
      fi
    done
  done
fi

if [ "$needs_update" = true ]; then
  python3 "$SCRIPT" --quiet >/dev/null 2>&1 || true
fi

exit 0
