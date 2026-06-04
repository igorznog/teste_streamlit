# Integração — portal FIAP On (skill tipo “FIAP Helper”)

Este documento alinha **automação no browser** (ex.: Claude Code + Playwright, ou scripts semelhantes) com este repositório: **`knowledge/`** + **`TASK_REGISTRY.md`**.

> A skill original do colega costuma viver em `~/.claude/skills/` (Claude Code). Aqui documentamos o **contrato** e os **limites** para o grupo; não é obrigatório usar automação.

## O que faz sentido automatizar

- **Ler** capítulos, enunciados e avisos no [FIAP On](https://on.fiap.com.br).
- **Exportar** texto para ficheiros Markdown em `knowledge/<disciplina>/` (pílulas, resumos).
- **Listar** prazos e itens pendentes para o aluno **atualizar** o `TASK_REGISTRY.md`.

## O que não deve ser promovido no repo do grupo

- **Submeter** fast tests, quizzes ou trabalhos **automaticamente** em nome do aluno.
- Copiar respostas para partilha em grupos da turma (risco de plágio/colusão e regras do portal).
- Guardar **RM, senha ou tokens** em ficheiros versionados no Git.

Fluxo seguro: automação **lê e gera rascunhos**; o aluno **revê**, **aprende** e **submete** o que for avaliativo.

## Credenciais

- Usar **variáveis de ambiente** ou ficheiro **local** fora do Git (ex.: `~/.config/fiap-on.env`, listado no `.gitignore` do teu clone pessoal).
- Nunca fazer commit de `.env` com senha.

## URLs úteis (estrutura típica Moodle)

Os IDs (`courseid`, `id`) **mudam** por turma e ano. Trata a lista abaixo como **exemplo de formato**, não como constantes fixas:

| Área | Padrão de URL (exemplo) |
|------|-------------------------|
| Login | `https://on.fiap.com.br` |
| Home | `/local/home/` |
| Jornada | `/local/jornada/index.php` |
| Conteúdo da fase | `/local/conteudocurso/index.php?courseid=...` |
| Capítulo HTML | `/mod/conteudoshtml/view.php?id=...` |
| Calendário | `/local/calendarioaluno` |

Para o teu curso: abre o portal no browser, copia os URLs reais e atualiza a tua skill ou script local.

## Onde gravar no repo

1. **Aulas / conceitos** → `knowledge/<nome_da_disciplina>/aulaNN_tema.md` (ver formato em [`knowledge/README.md`](../../knowledge/README.md)).
2. **Enunciado de task** → colar no chat + registar no `TASK_REGISTRY.md`; opcionalmente `tasks/taskN_nome/enunciado.md` (se o grupo acordar essa convenção).
3. **Quem faz o quê** → atualizar a tabela em [`GROUP.md`](../../GROUP.md) (commitada), para o grupo e a IA partilharem a mesma visão.

## Claude Code (skill)

Instalação típica descrita pelos autores da skill:

1. Pasta `~/.claude/skills/fiap-helper/` (nome pode variar).
2. Ficheiro `SKILL.md` com instruções; **sem** credenciais no texto que vá para o Git.

Comandos de exemplo que a skill pode expor ao utilizador (adaptar à vossa skill real):

- “resume o capítulo X para `knowledge/…`”
- “lista o que está pendente no portal e sugere linhas para o `TASK_REGISTRY.md`”

## Skill de projeto (Cursor)

Este repositório inclui uma skill de captura híbrida:
- `.cursor/skills/fiap-portal-capture/SKILL.md`

Template de colagem manual (fallback):
- `docs/templates/FIAP_TASK_CAPTURE_TEMPLATE.md`

Parser local da captura:
- `scripts/parse_fiap_task_capture.py`
- Workflow: `docs/workflows/08-captura-fiap-automatica.md`

Uso recomendado (em ordem de preferência):
1. **agent-browser** da Vercel Labs — CLI nativa cross-IDE com auth vault e skill oficial. Setup em `docs/integrations/agent-browser-fiap.md`.
2. Captura via Playwright local (`scripts/fiap_portal_capture.py`) — fallback Python puro.
3. Login assistido com sessão já aberta pelo aluno.
4. Template Ctrl+C/Ctrl+V (`docs/templates/FIAP_TASK_CAPTURE_TEMPLATE.md`) — fallback universal.

Setup completo Playwright: `docs/integrations/fiap-portal-capture-setup.md`.
Setup completo agent-browser: `docs/integrations/agent-browser-fiap.md`.

## Ligação ao assistente no VS Code / Copilot / outros

Anexa também [`FRAMEWORK.md`](../FRAMEWORK.md) para o modelo saber onde gravar conteúdo e como respeitar o registry.
