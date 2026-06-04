# FIAP Portal Capture — Setup e Uso (engine Playwright)

> Engine recomendada hoje: **agent-browser** da Vercel Labs
> ([docs/integrations/agent-browser-fiap.md](agent-browser-fiap.md)).
> Use o Playwright caseiro abaixo apenas como fallback (sem Node.js
> disponível, ou quando preferir Python puro).

Automação para capturar páginas do portal FIAP On com sessão persistente.
Funciona em qualquer IDE com agente (Cursor, Claude Code, Continue, Antigravity…)
porque o agente só precisa rodar comandos de shell.

## 1. Instalação (uma vez por máquina)

```bash
bash scripts/setup_fiap_capture.sh
```

O script cria `.venv-fiap-capture/` no repo e instala Playwright + Chromium.

> Linux/WSL2: se faltar lib de sistema, rode também:
> `python -m playwright install-deps chromium`

## 2. Login (uma vez por sessão de longa duração)

```bash
source .venv-fiap-capture/bin/activate
python scripts/fiap_portal_capture.py login
```

- Abre uma janela do Chromium.
- Você faz login normalmente, incluindo MFA.
- Quando estiver no dashboard, volte ao terminal e pressione ENTER.
- A sessão é salva em `~/.cache/fiap-portal-capture/profile/` (fora do Git).

## 3. Capturar uma página

```bash
python scripts/fiap_portal_capture.py capture \
    "https://on.fiap.com.br/local/conteudocurso/index.php?courseid=..." \
    --slug fase3-cap1
```

Saídas em `docs/validation/captures/`:

- `fase3-cap1_<timestamp>.html` — HTML completo renderizado.
- `fase3-cap1_<timestamp>.png` — screenshot full-page.
- `fase3-cap1_<timestamp>.txt` — texto visível.
- `fase3-cap1_<timestamp>.json` — metadados + links + imagens.

## 4. Capturar e preparar template de task

```bash
python scripts/fiap_portal_capture.py capture-task \
    "https://on.fiap.com.br/..." --slug fase3-cap1
```

Depois cole o `.txt` gerado em `docs/templates/FIAP_TASK_CAPTURE_TEMPLATE.md`
e rode o parser estruturado:

```bash
python scripts/parse_fiap_task_capture.py docs/templates/FIAP_TASK_CAPTURE_TEMPLATE.md
```

## 5. Atalhos para o agente (Cursor / Claude Code / outros)

A skill `fiap-portal-capture` está em `.cursor/skills/fiap-portal-capture/SKILL.md`.
Para usar em outras IDEs, copie a pasta:

| IDE / Agente        | Caminho de instalação                                |
|---------------------|------------------------------------------------------|
| Cursor (projeto)    | `.cursor/skills/fiap-portal-capture/`                |
| Cursor (pessoal)    | `~/.cursor/skills/fiap-portal-capture/`              |
| Claude Code         | `~/.claude/skills/fiap-portal-capture/`              |
| Continue/Antigravity| Anexe `SKILL.md` no contexto da conversa             |
| Qualquer outro      | Cole o conteúdo de `SKILL.md` no prompt do agente    |

## 6. Segurança

- Senha NUNCA é digitada no agente nem em arquivo.
- Sessão fica em `~/.cache/fiap-portal-capture/` (já em `.gitignore`).
- Submissão de quizzes/fast tests permanece manual.
- Se sessão expirar, basta rodar `login` de novo.

## 7. Troubleshooting

| Sintoma                              | Solução                                                   |
|--------------------------------------|-----------------------------------------------------------|
| `playwright not installed`           | Rode `bash scripts/setup_fiap_capture.sh`.                |
| Chromium não abre no WSL2            | Tenha um servidor X (WSLg já basta no Windows 11).        |
| Página vem em branco                 | Rode `login` de novo; sessão pode ter expirado.           |
| Conteúdo dinâmico não aparece        | Suba `--wait-ms 4000`.                                    |
| Quer ver passo a passo               | Não passe `--headless`; o navegador abre na frente.       |
