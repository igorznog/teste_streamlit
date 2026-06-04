---
name: fiap-portal-capture
description: Captura conteúdo completo de páginas do portal FIAP On (texto, imagens, disclaimers, links) com três engines — agent-browser da Vercel (cross-IDE), Playwright local em Python, ou colagem manual estruturada. Use quando o usuário pedir para logar na FIAP, extrair, copiar, ingerir ou registrar enunciados/aulas do portal.
disable-model-invocation: true
---

# FIAP Portal Capture

Skill portátil para capturar páginas do portal FIAP On
(<https://on.fiap.com.br>) com 100% de fidelidade — texto, screenshot,
imagens, links e disclaimers. Funciona em Cursor, Claude Code, Codex,
Gemini CLI, Copilot, Windsurf e qualquer IDE com agente que execute shell.

## Quando ativar

- "loga na FIAP", "extrai a página", "copia o capítulo X", "ingere a aula".
- Antes de criar `SPEC.md` para uma task cujo enunciado está no portal.
- Quando o aluno cola uma URL do `on.fiap.com.br`.

## Regras de segurança

- NUNCA pedir senha em texto no chat. Use o auth vault do agent-browser.
- NUNCA salvar credenciais em arquivos versionados (`.gitignore` já cobre).
- MFA/CAPTCHA são concluídos pelo aluno.
- Submissão de fast tests/quizzes é sempre humana.
- Restringir navegação ao domínio FIAP com `--allowed-domains`.

## Engine 1 — agent-browser (preferencial)

CLI nativa Rust da Vercel Labs. Setup em qualquer plataforma e IDE.
Detalhes completos em `docs/integrations/agent-browser-fiap.md`.

### Setup (uma vez)

```bash
npm install -g agent-browser     # prefix ~/.npm-global (sem sudo se configurado)
agent-browser install            # baixa Chrome for Testing (~175 MB)
agent-browser doctor             # 6 pass / 0 warn / 0 fail esperado
npx -y skills add vercel-labs/agent-browser   # instala skill cross-IDE em .agents/skills/
```

> Validado neste workspace em 17/05/2026 com `agent-browser 0.27.0` e
> Chrome 148. Evidência em `docs/validation/agent_browser_smoke_test.md`.

### Login (uma vez)

```bash
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
echo "<senha>" | agent-browser auth save fiap-on \
    --url https://on.fiap.com.br/login/index.php \
    --username <usuario> --password-stdin
agent-browser auth login fiap-on
```

### Captura

**Modo padrão (e-books PDF de todas as fases liberadas):**

```bash
python3 scripts/fiap_capture_all_phases.py
```

Por que e-book PDF é o padrão? Todo capítulo do portal FIAP On oferta um PDF
canônico com o conteúdo completo da aula. PDF é mais rápido (1 requisição por
capítulo) e auto-suficiente comparado a iterar slides HTML.

Flags úteis:

| Flag | Quando usar |
|------|-------------|
| `--phases 1,3` | Capturar apenas fases específicas (CSV) |
| `--max-chapters N` | Smoke test rápido (N caps por fase) |
| `--slides` | Também capturar conteúdo HTML iterando slides (LENTO; só sob pedido explícito) |
| `--assets` | Também baixar ZIPs de assets quando houver |
| `--no-pdf` | Não baixar PDFs (usar com `--slides` ou `--assets`) |
| `--keep-output` | Preservar capturas anteriores (default limpa a pasta) |

Saída em `docs/validation/captures/fases/<faseN>/cap<NN>_<slug>/<arquivo>.pdf`
+ `INDEX.json` consolidado. Detalhes em `docs/validation/fiap_pdfs_captured.md`.

**Modo ad-hoc (uma página específica):**

```bash
agent-browser --session-name fiap-on auth login fiap-on
agent-browser --session-name fiap-on open "<URL>"
agent-browser --session-name fiap-on wait --load networkidle
agent-browser --session-name fiap-on snapshot -i --urls
agent-browser --session-name fiap-on screenshot --full docs/validation/captures/<slug>.png
```

### Reuso do Brave já logado

```bash
agent-browser \
  --executable-path /usr/bin/brave-browser \
  --profile "$HOME/.config/BraveSoftware/Brave-Browser" \
  open https://on.fiap.com.br/local/conteudocurso/
```

## Engine 2 — Playwright local (Python)

Fallback quando o agent-browser não está disponível.

```bash
bash scripts/setup_fiap_capture.sh
source .venv-fiap-capture/bin/activate
python scripts/fiap_portal_capture.py login
python scripts/fiap_portal_capture.py capture "<URL>" --slug <nome-curto>
```

Saída em `docs/validation/captures/<slug>_<timestamp>.{html,png,txt,json}`.

## Engine 3 — Ctrl+C/Ctrl+V estruturado (fallback universal)

Quando nenhuma automação está disponível, pedir colagem no template
`docs/templates/FIAP_TASK_CAPTURE_TEMPLATE.md`:

```markdown
[METADADOS]
URL:
Disciplina/Fase/Cap:
Data/Hora da cópia:

[TEXTO PRINCIPAL]
(colar tudo, sem limpar)

[DISCLAIMERS E AVISOS]
(colar literalmente todos os blocos de aviso)

[IMAGENS]
- img1: [descrição] | [texto visível na imagem]

[LINKS/ANEXOS]
- [nome] - [URL]
```

## Pipeline padrão (qualquer engine)

```bash
python3 scripts/parse_fiap_task_capture.py docs/templates/FIAP_TASK_CAPTURE_TEMPLATE.md
```

Gera `docs/validation/fiap_capture_parsed.{md,json}` estruturado com
metadados, capítulos, progresso e atividade.

## Checklist de completude (100%)

- [ ] URL e data/hora registrados.
- [ ] Texto principal completo.
- [ ] Disclaimers/avisos incluídos.
- [ ] Imagens listadas (descrição + texto visível).
- [ ] Links/anexos listados.
- [ ] Trechos cortados sinalizados explicitamente.

## Saída padrão da skill

1. Captura bruta em `docs/validation/captures/` (ignorada pelo Git).
2. Versão estruturada em `docs/validation/fiap_capture_parsed.{md,json}`.
3. Pílula em `knowledge/<disciplina>/aulaNN_tema.md` quando solicitado.
4. Atualização do `TASK_REGISTRY.md` com status e pendências.

## Instalação em outras IDEs

Duas skills convivem no projeto:

- `fiap-portal-capture` (esta) — convenções FIAP, parser, knowledge base.
- `agent-browser` — workflow genérico de browser, instalada pelo `skills.sh`.

| IDE / Agente         | Caminho `fiap-portal-capture`                          | `agent-browser`                                   |
|----------------------|--------------------------------------------------------|---------------------------------------------------|
| Cursor (projeto)     | `.cursor/skills/fiap-portal-capture/SKILL.md`          | `.agents/skills/agent-browser/SKILL.md` (auto)    |
| Cursor (pessoal)     | `~/.cursor/skills/fiap-portal-capture/SKILL.md`        | idem após `npx skills add ...` no $HOME           |
| Claude Code          | `~/.claude/skills/fiap-portal-capture/SKILL.md`        | `~/.claude/skills/agent-browser/SKILL.md` (auto)  |
| Codex / Gemini CLI / Goose / OpenCode / Windsurf / Copilot | Pelo `npx skills add` (formato padrão `.agents/skills/`) | idem |
| Outras (Continue…)   | Anexar este `SKILL.md` no contexto                     | rodar `agent-browser skills get core`             |

Para copiar `fiap-portal-capture` para Claude Code pessoal:

```bash
mkdir -p ~/.claude/skills/fiap-portal-capture
cp .cursor/skills/fiap-portal-capture/SKILL.md ~/.claude/skills/fiap-portal-capture/
```
