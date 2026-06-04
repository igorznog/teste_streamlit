#!/usr/bin/env bash
# Setup tudo-em-um da automação do portal FIAP para o grupo.
#
# Faz:
#   1. Verifica Node.js (instrui instalação se faltar)
#   2. Configura prefix do npm em $HOME (evita sudo)
#   3. Instala agent-browser (CLI Rust nativa)
#   4. Baixa Chrome de teste
#   5. (Opcional) Instala libs do Chrome (Linux/WSL)
#   6. Roda diagnóstico
#   7. Instala skill oficial agent-browser
#   8. Copia skill fiap-portal-capture para a IDE escolhida
#   9. (Opcional) Configura auth vault com sua credencial FIAP
#  10. Mostra próximos passos
#
# Roda quantas vezes quiser: é idempotente.

set -euo pipefail

# ---------- helpers de UI ----------
if [[ -t 1 ]]; then
  GREEN=$'\033[0;32m'; RED=$'\033[0;31m'; YELLOW=$'\033[1;33m'
  BLUE=$'\033[0;34m';  BOLD=$'\033[1m';  NC=$'\033[0m'
else
  GREEN=""; RED=""; YELLOW=""; BLUE=""; BOLD=""; NC=""
fi
say()  { printf '%s==>%s %s\n' "$BLUE"  "$NC" "$*"; }
ok()   { printf '%s✓%s %s\n'   "$GREEN" "$NC" "$*"; }
warn() { printf '%s⚠%s %s\n'   "$YELLOW" "$NC" "$*"; }
err()  { printf '%s✗%s %s\n'   "$RED"   "$NC" "$*" >&2; }
ask() {
  local prompt="$1"; local default="${2:-}"; local var
  if [[ -n "$default" ]]; then
    read -r -p "${BOLD}?${NC} ${prompt} [${default}]: " var
    printf '%s' "${var:-$default}"
  else
    read -r -p "${BOLD}?${NC} ${prompt}: " var
    printf '%s' "$var"
  fi
}
ask_yes_no() {
  local prompt="$1"; local default="${2:-n}"; local ans
  read -r -p "${BOLD}?${NC} ${prompt} (s/n) [${default}]: " ans
  ans="${ans:-$default}"
  [[ "${ans,,}" =~ ^(s|sim|y|yes)$ ]]
}
banner() {
  echo
  echo "==========================================================="
  printf '  %sFIAP Automation Setup%s — captura automática do portal\n' "$BOLD" "$NC"
  echo "==========================================================="
  echo
}

# ---------- início ----------
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

banner
say "Esse script prepara seu computador para o assistente abrir o"
say "portal FIAP sozinho. Leva uns 3-5 minutos na primeira vez."
echo

# 1) Detectar SO
OS_KIND="unknown"
case "$(uname -s)" in
  Darwin*) OS_KIND="mac";;
  Linux*)
    if grep -qi microsoft /proc/version 2>/dev/null; then
      OS_KIND="wsl"
    else
      OS_KIND="linux"
    fi
    ;;
esac
ok "Sistema: $OS_KIND"

# 2) Node.js
if ! command -v node >/dev/null 2>&1; then
  err "Node.js não encontrado."
  echo
  echo "Instale Node 20 antes de continuar:"
  case "$OS_KIND" in
    mac)
      echo "  brew install node@20"
      ;;
    *)
      echo "  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash"
      echo "  source ~/.bashrc"
      echo "  nvm install --lts"
      ;;
  esac
  exit 1
fi

NODE_MAJOR=$(node -p 'process.versions.node.split(".")[0]')
if [[ "$NODE_MAJOR" -lt 18 ]]; then
  err "Node.js $NODE_MAJOR é antigo demais. Atualize para Node 20 (use nvm)."
  exit 1
fi
ok "Node.js $(node --version)"

# 3) Prefix npm em $HOME (zero sudo)
CURRENT_PREFIX="$(npm prefix -g 2>/dev/null || echo "")"
if [[ "$CURRENT_PREFIX" != "$HOME"* ]]; then
  say "Configurando npm para instalar pacotes globais sem sudo..."
  mkdir -p "$HOME/.npm-global"
  npm config set prefix "$HOME/.npm-global"
  case ":$PATH:" in
    *:"$HOME/.npm-global/bin":*) :;;
    *)
      export PATH="$HOME/.npm-global/bin:$PATH"
      EXPORT_PATH_LINE='export PATH="$HOME/.npm-global/bin:$PATH"'
      for RC in "$HOME/.bashrc" "$HOME/.zshrc"; do
        [[ -f "$RC" ]] || continue
        if ! grep -qxF "$EXPORT_PATH_LINE" "$RC"; then
          printf '\n# Adicionado pelo setup_fiap_automation.sh\n%s\n' "$EXPORT_PATH_LINE" >> "$RC"
        fi
      done
      ;;
  esac
  ok "Prefix do npm em $HOME/.npm-global"
fi

# 4) agent-browser
if command -v agent-browser >/dev/null 2>&1; then
  ok "agent-browser já instalado ($(agent-browser --version))"
else
  say "Instalando agent-browser (~1 min)..."
  npm install -g agent-browser >/dev/null
  if ! command -v agent-browser >/dev/null 2>&1; then
    err "agent-browser não ficou no PATH. Abra um terminal novo e rode o script de novo."
    exit 1
  fi
  ok "agent-browser $(agent-browser --version)"
fi

# 5) Chrome de teste
CHROME_DIR="$HOME/.agent-browser/browsers"
if [[ -d "$CHROME_DIR" ]] && ls "$CHROME_DIR" 2>/dev/null | grep -q chrome; then
  ok "Chrome de teste já baixado"
else
  say "Baixando Chrome de teste (~175 MB)..."
  agent-browser install
fi

# 6) Libs do sistema (Linux/WSL)
if [[ "$OS_KIND" == "linux" || "$OS_KIND" == "wsl" ]]; then
  if ask_yes_no "Tentar instalar libs do Chrome (precisa de sudo, opcional)?" "n"; then
    agent-browser install --with-deps || warn "install-deps falhou; pode funcionar mesmo assim"
  fi
fi

# 7) Doctor
say "Validando instalação..."
if agent-browser doctor --offline --quick | tee /tmp/ab_doctor.log | grep -q "0 fail"; then
  ok "Diagnóstico OK"
else
  warn "Doctor reportou problemas. Veja /tmp/ab_doctor.log e rode: agent-browser doctor --fix"
fi

# 8) Skill oficial agent-browser
if [[ -f .agents/skills/agent-browser/SKILL.md ]]; then
  ok "Skill oficial agent-browser já instalada"
else
  say "Instalando skill oficial agent-browser..."
  if npx -y skills add vercel-labs/agent-browser >/dev/null 2>&1; then
    ok "Skill agent-browser em .agents/skills/agent-browser/"
  else
    warn "Falhou. Rode manualmente depois: npx skills add vercel-labs/agent-browser"
  fi
fi

# 9) Skill fiap-portal-capture para a IDE escolhida
SOURCE_SKILL="$REPO_ROOT/.cursor/skills/fiap-portal-capture/SKILL.md"
if [[ -f "$SOURCE_SKILL" ]]; then
  echo
  say "Em qual IDE você usa o assistente?"
  echo "  1) Cursor                  (skill já no .cursor/skills/, nada a fazer)"
  echo "  2) Claude Code             (copia para ~/.claude/skills/)"
  echo "  3) Cursor + Claude Code"
  echo "  4) Outras (Codex, Gemini, Copilot…) — anexar SKILL.md no chat"
  CHOICE=$(ask "Escolha 1-4" "1")
  case "$CHOICE" in
    2|3)
      mkdir -p "$HOME/.claude/skills/fiap-portal-capture"
      cp "$SOURCE_SKILL" "$HOME/.claude/skills/fiap-portal-capture/SKILL.md"
      ok "Skill copiada para ~/.claude/skills/fiap-portal-capture/"
      ;;
    4)
      echo "  Para outras IDEs, anexe no chat: $SOURCE_SKILL"
      ;;
  esac
fi

# 10) Auth vault FIAP (opcional)
echo
say "Configurar login automático do portal FIAP?"
echo "   - Sua senha é criptografada localmente (AES-256-GCM)."
echo "   - O assistente NUNCA recebe a senha em texto."
echo "   - Você pode pular agora e configurar depois com 'agent-browser auth save'."
if ask_yes_no "Configurar agora?" "s"; then
  KEY_FILE="$HOME/.agent-browser/.encryption-key"
  if [[ ! -f "$KEY_FILE" ]]; then
    mkdir -p "$(dirname "$KEY_FILE")"
    if command -v openssl >/dev/null 2>&1; then
      openssl rand -hex 32 > "$KEY_FILE"
    else
      head -c 32 /dev/urandom | xxd -p -c 64 > "$KEY_FILE"
    fi
    chmod 600 "$KEY_FILE"
    ok "Chave de criptografia gerada em $KEY_FILE"
  fi
  export AGENT_BROWSER_ENCRYPTION_KEY="$(cat "$KEY_FILE")"

  USERNAME=$(ask "Seu RM ou usuário FIAP")
  echo
  echo "Digite a senha (não será exibida na tela):"
  read -r -s -p "Senha FIAP: " FIAP_PASS
  echo
  if [[ -z "${FIAP_PASS:-}" ]]; then
    warn "Senha em branco — pulando configuração do vault."
  else
    if printf '%s' "$FIAP_PASS" | agent-browser auth save fiap-on \
        --url https://on.fiap.com.br/login/index.php \
        --username "$USERNAME" \
        --password-stdin >/dev/null 2>&1; then
      ok "Credencial salva no vault como 'fiap-on'"
    else
      err "Falha ao salvar no vault. Tente manualmente:"
      echo "  echo SUA_SENHA | agent-browser auth save fiap-on \\"
      echo "    --url https://on.fiap.com.br/login/index.php \\"
      echo "    --username SEU_RM --password-stdin"
    fi
    unset FIAP_PASS
  fi

  # Persistir variável de ambiente
  EXPORT_KEY_LINE='export AGENT_BROWSER_ENCRYPTION_KEY="$(cat "$HOME/.agent-browser/.encryption-key")"'
  for RC in "$HOME/.bashrc" "$HOME/.zshrc"; do
    [[ -f "$RC" ]] || continue
    if ! grep -qxF "$EXPORT_KEY_LINE" "$RC"; then
      printf '\n# Chave do agent-browser auth vault\n%s\n' "$EXPORT_KEY_LINE" >> "$RC"
      ok "AGENT_BROWSER_ENCRYPTION_KEY adicionado ao $RC"
    fi
  done
fi

# 11) Final
echo
echo "==========================================================="
ok "Setup concluído!"
echo "==========================================================="
echo
printf '%sAbra um terminal novo%s (ou rode: source ~/.bashrc) e teste:\n' "$BOLD" "$NC"
echo
echo "  agent-browser auth login fiap-on        # loga no portal"
echo "  agent-browser open https://on.fiap.com.br/local/home/"
echo "  agent-browser snapshot -i               # lê a página"
echo "  agent-browser screenshot --full saida.png"
echo "  agent-browser close"
echo
printf '%sNo chat do seu assistente, peça por exemplo:%s\n' "$BOLD" "$NC"
echo "  \"Use a skill fiap-portal-capture para capturar essa URL: …\""
echo
printf '%sDocumentação:%s\n' "$BOLD" "$NC"
echo "  docs/integrations/agent-browser-fiap.md   (guia completo)"
echo "  docs/QUICKSTART_AUTOMACAO.md              (versão 1 página)"
echo "  docs/validation/agent_browser_smoke_test.md (evidência do teste real)"
echo
