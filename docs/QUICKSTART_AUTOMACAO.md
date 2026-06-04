# Quickstart — Automação do Portal FIAP

Guia para qualquer colega do grupo que **não usa terminal todo dia**.

## Em 1 comando

Dentro da pasta do repositório, abra o terminal e rode:

```bash
bash scripts/setup_fiap_automation.sh
```

O script faz perguntas amigáveis em português e cuida do resto.

Ele instala:

- `agent-browser` (a CLI que abre o navegador para o assistente).
- Chrome de teste (155 MB, leva 1 min).
- Skill oficial do `agent-browser` (cross-IDE).
- Skill `fiap-portal-capture` no IDE que você escolher (Cursor ou Claude Code).
- Opcional: salva sua senha do portal no cofre criptografado local.

> No primeiro uso ele pode pedir para você **abrir um terminal novo**
> depois — basta fechar e abrir de novo.

## Pré-requisitos

Só **um** pré-requisito antes de rodar:

- **Node.js 20+** instalado. Como instalar se não tiver:

  | Sistema | Comando |
  |---------|---------|
  | macOS   | `brew install node@20` |
  | Linux / WSL2 | `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh \| bash` depois `source ~/.bashrc && nvm install --lts` |
  | Windows | Baixe o instalador em <https://nodejs.org/> |

Se você já usa Cursor / VS Code, **provavelmente já tem Node**.

## Como usar depois

No chat do seu assistente (Cursor, Claude Code, etc.), peça:

> "Use a skill `fiap-portal-capture` para capturar a página
> `https://on.fiap.com.br/local/conteudocurso/...` e salvar em
> `docs/validation/captures/`."

O assistente vai chamar o `agent-browser`, fazer login (sua senha está no
cofre, ele nunca vê em texto), tirar screenshot, salvar o conteúdo e
opcionalmente gerar uma pílula em `knowledge/`.

## Não quer login automático?

Sem problema. Pule o passo 10 do script (auth vault) e use:

1. **Modo manual**: copie a página com `Ctrl+A → Ctrl+C` e cole no chat
   usando o template em `docs/templates/FIAP_TASK_CAPTURE_TEMPLATE.md`.
2. **Modo perfil Brave**: rode `agent-browser` apontando para o seu Brave
   já logado. Veja `docs/integrations/agent-browser-fiap.md` §3.2.

## Resolução de problemas

| Sintoma | O que fazer |
|---------|-------------|
| `command not found: agent-browser` | Abra um terminal novo ou `source ~/.bashrc`. |
| `npm install -g` pede sudo | O script já configura `~/.npm-global` — rode-o de novo. |
| Chrome não abre no WSL2 | Você precisa do WSLg (Windows 11) ou rode `--with-deps`. |
| Portal pede MFA / Captcha | Conclua manualmente; sessão fica salva depois. |
| Quer apagar tudo | `rm -rf ~/.agent-browser ~/.npm-global/bin/agent-browser` |

## Segurança

- Senha fica em `~/.agent-browser/` criptografada (AES-256-GCM).
- Nada disso vai para o Git (`.gitignore` cobre).
- Submissão de Fast Tests / quizzes continua manual — bom senso primeiro.

## Quer ler mais?

- `docs/integrations/agent-browser-fiap.md` — guia técnico completo.
- `.cursor/skills/fiap-portal-capture/SKILL.md` — a skill em si.
- `docs/validation/agent_browser_smoke_test.md` — evidência do teste real.
