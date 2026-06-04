# Framework FIAP — workspace para entregas e estudo

**Começa aqui:** guia passo a passo para o grupo → **[`SETUP.md`](SETUP.md)** e [`docs/workflows/00-onboarding-colega.md`](docs/workflows/00-onboarding-colega.md) (nome, `GROUP.md`, `LOCAL.md`, primeira mensagem à IA).

Repositório mínimo para disciplinas **FIAP**: registo de tasks ([`TASK_REGISTRY.md`](TASK_REGISTRY.md)), identificação do grupo ([`GROUP.md`](GROUP.md)), base de conhecimento ([`knowledge/`](knowledge/)) e regras para assistentes de IA.

O fluxo é **spec-driven**: toda task vira uma spec em `specs/` antes da execução em `tasks/`. Para trabalho em grupo, a divisão fica registrada em `SPLIT.md` e a integração em `INTEGRATION.md`.

## IDE e assistentes suportados

O fluxo de trabalho **comum** a todos está em **[`docs/FRAMEWORK.md`](docs/FRAMEWORK.md)** (agnóstico de IDE).  
Recomendação: **abrir ou anexar** esse ficheiro na primeira mensagem quando o assistente não ler o projeto sozinho.

| IDE / ferramenta | Como aplicar este repo |
|------------------|-------------------------|
| **Cursor** | Abre a pasta no Cursor; [`.cursorrules`](.cursorrules) e [`.cursor/rules/`](.cursor/rules/) são carregados automaticamente. |
| **VS Code + GitHub Copilot** | Abre a pasta no VS Code; o Copilot usa [`.github/copilot-instructions.md`](.github/copilot-instructions.md). Para contexto completo, anexa também `docs/FRAMEWORK.md` em conversas longas. |
| **Claude Code** | Anexa `docs/FRAMEWORK.md`; skills opcionais (ex.: portal FIAP) em `~/.claude/skills/` — ver [integração portal](docs/integrations/fiap-portal-helper.md). |
| **Google Antigravity** (ou outro editor com chat) | Anexa `docs/FRAMEWORK.md` + `TASK_REGISTRY.md` ao iniciar a sessão. |

## Jornada recomendada

1. **Onboarding:** configurar identidade e grupo com [`SETUP.md`](SETUP.md).
2. **Fonte oficial:** capturar task/aula pelo portal FIAP ou pelo template manual.
3. **Spec:** criar `SPEC.md` e `WORKPLAN.md` antes de executar.
4. **Execução:** trabalhar solo ou por partes do grupo.
5. **Estudo:** gerar study pack para prova, defesa e NotebookLM.
6. **Entrega:** revisar segurança, empacotar e submeter manualmente no portal.

## Painéis rápidos

Para mandar o repositório no WhatsApp e dar contexto imediato ao grupo:

- [`docs/dashboard/index.html`](docs/dashboard/index.html) — entrada visual central do workflow.
- [`docs/dashboard/grupo.html`](docs/dashboard/grupo.html) — visão geral das tasks, pendências, membros e links úteis.
- [`docs/dashboard/individual.html`](docs/dashboard/individual.html) — visão por integrante, sem depender de `LOCAL.md`.
- [`docs/dashboard/registry.html`](docs/dashboard/registry.html) — versão visual e filtrável do `TASK_REGISTRY.md`.

Os painéis são snapshots estáticos gerados a partir de `TASK_REGISTRY.md` e `GROUP.md`. Depois de mudar status, rode:

```bash
python scripts/update_workflow_dashboard.py
```

No Cursor, o projeto também tem um hook silencioso que tenta sincronizar esses HTMLs após edições. Em outros agentes/IDEs, use a versão sem saída para não poluir o contexto:

```bash
python scripts/update_workflow_dashboard.py --quiet
```

## Setup rápido

1. Lê **[`SETUP.md`](SETUP.md)** (integração de colegas em 5 minutos).
2. Clone (ou fork + clone) este repositório.
3. Abre a pasta no teu IDE.
4. Roda `python setup.py`.
5. No **Cursor**, se quiseres, edita [`.cursorrules`](.cursorrules): substitui `{{ALUNO}}` pelo teu nome.
6. Em **qualquer IDE**, mantém [`TASK_REGISTRY.md`](TASK_REGISTRY.md) atualizado.
7. Se for novo no grupo, segue [`docs/workflows/00-onboarding-colega.md`](docs/workflows/00-onboarding-colega.md).

## Como usar no chat da IA

O uso principal é simples: **cola a task ou a aula no chat** e pede para o framework processar.

### Processar uma task/challenge pelo portal

Use quando tiver o enunciado da atividade:

```text
Leia GROUP.md, LOCAL.md, TASK_REGISTRY.md e docs/workflows/09-task-portal-first.md.
Vou iniciar uma task da FIAP.
Use a fonte oficial do portal ou minha captura manual,
classifique o tipo de entrega, pergunte se é solo ou grupo,
crie SPEC.md e WORKPLAN.md antes de implementar.

[cole aqui a URL, captura automatica ou enunciado completo]
```

Se já souber que é grupo:

```text
Esta task é em grupo. Eu quero fazer apenas minha parte.
Use GROUP.md e LOCAL.md para identificar quem eu sou.
Crie/atualize SPEC.md, SPLIT.md, WORKPLAN.md e INTEGRATION.md antes de implementar.

[cole aqui o enunciado completo ou a parte combinada]
```

### Ingerir uma aula ou gerar study pack

Use para **PDF da aula** ou para texto copiado com `Ctrl+C` da página da aula:

```text
Leia docs/workflows/01-ingestao-aula.md.
Vou enviar o conteúdo de uma aula da FIAP.
Transforme em pílula em knowledge/<disciplina>/,
atualize flashcards.md e relacione com possíveis tasks.

[anexe o PDF ou cole o texto copiado da página]
```

Para estudar com active recall, defesa oral e NotebookLM:

```text
Leia docs/workflows/10-study-pack-generation.md.
Use as fontes oficiais capturadas para gerar um study pack moderno:
Cornell, Feynman, mapa conceitual, quiz bank, flashcards,
defesa oral e plano SRS.
```

### Revisar ou integrar grupo

```text
Leia SPEC.md, SPLIT.md, INTEGRATION.md e REVIEW.md desta task.
Quero revisar a parte de [nome] / assumir a parte [Px] / integrar todos os PRs.
Mostre gaps, riscos e próximos passos Git.
```

## Onde colocar cada trabalho

- Sugestão: `tasks/taskN_nome_curto/` para cada entrega.
- Specs e divisões ficam em `specs/taskN_nome_curto/`.
- Regista sempre a task em `TASK_REGISTRY.md` (status, checklist, entregáveis).

## Três formas de usar (solo ou grupo)

| Cenário | Quando | Git |
|--------|--------|-----|
| **Solo** | Atividade individual | `main` ou uma branch; commit quando quiseres versionar. |
| **Grupo — só a tua parte** | Divisão por ficheiros (ex.: um notebook por pessoa) | Branch por pessoa + Pull Request para `main`. |
| **Grupo — artefato único** | Um entregável conjunto | Mesmo fluxo de branches + PR; evita dois editores no mesmo ficheiro em simultâneo. |

## Atualizar o framework

```bash
git checkout main
git pull origin main
```

## Estudo móvel (opcional)

```bash
export FIAP_KNOWLEDGE_DEST="/caminho/para/FIAP_Knowledge"
./scripts/sync_knowledge.sh
```

Sem variável, a cópia vai para `~/FIAP_Knowledge`.

## NotebookLM (opcional)

Gere fontes limpas para importar manualmente no NotebookLM comum:

```bash
python scripts/export_notebooklm_pack.py --source knowledge/<disciplina> --dest ~/FIAP_NotebookLM/<tema>
```

Leia [`docs/integrations/notebooklm.md`](docs/integrations/notebooklm.md) antes de exportar fontes autenticadas, PDFs ou dados pessoais.

## Workflows principais

- [`docs/workflows/00-onboarding-colega.md`](docs/workflows/00-onboarding-colega.md) — entrada de colegas.
- [`docs/workflows/09-task-portal-first.md`](docs/workflows/09-task-portal-first.md) — task oficial do portal para spec.
- [`docs/workflows/10-study-pack-generation.md`](docs/workflows/10-study-pack-generation.md) — estudo moderno e defesa.
- [`docs/templates/FIAP_DELIVERY_TYPES.md`](docs/templates/FIAP_DELIVERY_TYPES.md) — matriz de tipos de entrega.
- [`docs/templates/SAFETY_PII_COPYRIGHT_CHECKLIST.md`](docs/templates/SAFETY_PII_COPYRIGHT_CHECKLIST.md) — revisao antes de publicar/exportar.

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md).


## Versão Pública Sanitizada

Este repositório contém o workflow, regras, templates, scripts e exemplos reutilizáveis para organizar entregas FIAP com agentes de IA.

Não são versionados:

- `LOCAL.md` com identificação pessoal do clone.
- Senhas, `.env`, chaves ou vault do `agent-browser`.
- Capturas autenticadas do portal, PDFs de aulas e entregas reais com dados pessoais.
- Notebooks ou arquivos com nome/RM de alunos.

Para começar:

1. Preencha `GROUP.md`.
2. Copie `LOCAL.example.md` para `LOCAL.md` e preencha seus dados localmente.
3. Rode `bash scripts/setup_fiap_automation.sh` se quiser automação FIAP.
4. Use `docs/templates/FIAP_TASK_CAPTURE_TEMPLATE.md` ou a skill `fiap-portal-capture`.
