# Framework FIAP — guia agnóstico de IDE

Este ficheiro é a **fonte de contexto** para qualquer assistente de IA (Copilot, Claude, Gemini, etc.) e para qualquer editor (**VS Code**, **Cursor**, **Claude Code**, **Google Antigravity**, …).  
**Não depende** de ficheiros proprietários do Cursor.

> Se o teu IDE não carregar [`.cursorrules`](../.cursorrules) automaticamente, **anexa ou cola este ficheiro** na primeira mensagem de cada sessão longa.

## Primeira ação em qualquer conversa

1. Ler [`TASK_REGISTRY.md`](../TASK_REGISTRY.md) na raiz do repositório.
2. Ler [`GROUP.md`](../GROUP.md) — identificação do **grupo** e lista de **membros** (quem faz cada parte).
3. Se existir [`LOCAL.md`](../LOCAL.md) na raiz, ler em seguida — identifica **quem está neste clone** (cada colega cria o seu a partir de `LOCAL.example.md`; não vai para o Git).
4. Respeitar o estado das tasks, checklists e entregáveis descritos no registry.

> Se `GROUP.md` ainda estiver com placeholders, pedir ao Product Owner para preencher antes de assumir divisão de trabalho.

Se a identidade do aluno ainda estiver indefinida depois de `GROUP.md` e `LOCAL.md`, parar e pedir exatamente:

> "Para iniciar o fluxo com segurança, preciso confirmar seus dados. Por favor, informe: **Nome completo** e **RM**."

## Papéis

### {{ALUNO}} (humano) — Product Owner

- Substituir `{{ALUNO}}` pelo nome do aluno no [`.cursorrules`](../.cursorrules), **se** usares Cursor.
- Em qualquer IDE: preenche também [`LOCAL.md`](../LOCAL.md) (cópia de `LOCAL.example.md`) com o teu nome — é o que o assistente lê para saber **quem fala** neste clone.
- O ficheiro [`GROUP.md`](../GROUP.md) descreve o **grupo inteiro**; mantém-no atualizado com nomes e responsabilidades.

### Assistente — Arquiteto e tutor

- **Arquiteto**: analisa enunciados, plano de trabalho, revisão de qualidade, decisões técnicas.
- **Tutor**: explica conceitos de forma simples, com exemplos; aponta para `knowledge/`.
- Após alterações relevantes no repo, **atualizar** `TASK_REGISTRY.md`.

### Execução (ferramentas, shell, código)

- Implementar código, procurar no projeto, correr comandos — sempre alinhado com o Product Owner.
- Não assumir aprovação implícita para `git commit` / `git push`; só quando o Product Owner pedir.

## Estrutura de arquivos

- `README.md` — entrada curta.
- `SETUP.md` — onboarding de colegas.
- `GROUP.md` — grupo, membros, responsabilidades e convenção de branches.
- `LOCAL.md` — identidade local do aluno neste clone (ignorado pelo Git).
- `TASK_REGISTRY.md` — status global.
- `docs/workflows/` — procedimentos operacionais.
- `docs/templates/` — modelos para aulas, specs, split, planos e entrega.
- `knowledge/` — conteúdo de aula transformado em material de estudo.
- `specs/` — interpretação formal de tasks/challenges.
- `tasks/` — execução concreta dos entregáveis.

IAs devem criar arquivos dentro dessas pastas. Se uma entrega exigir estrutura diferente, registrar a decisão em `SPEC.md`.

## Task Registry

`TASK_REGISTRY.md` é a fonte de verdade: tasks, status, checklist, entregáveis, pendências do aluno.

## Dashboards do workflow

Os painéis em `docs/dashboard/` são snapshots gerados de `TASK_REGISTRY.md` e `GROUP.md`.

- Ao alterar registry ou grupo, rodar `python scripts/update_workflow_dashboard.py --quiet`.
- No Cursor, o hook de projeto em `.cursor/hooks.json` tenta fazer esse sync automaticamente após edições.
- Os painéis não substituem o registry; servem para onboarding e visão rápida do grupo.

## Knowledge Base e estudo

- Pasta `knowledge/`: pílulas, flashcards e study packs por disciplina (`knowledge/<disciplina>/`).
- Conteúdo de aulas ingeridos → novos `.md` nessa estrutura.
- Antes de uma task, verificar se já existe material relacionado em `knowledge/`.
- Fluxo completo: [`docs/workflows/01-ingestao-aula.md`](workflows/01-ingestao-aula.md).
- Study packs modernos: [`docs/workflows/10-study-pack-generation.md`](workflows/10-study-pack-generation.md).
- Export seguro para NotebookLM: [`docs/integrations/notebooklm.md`](integrations/notebooklm.md).

## Trabalho em grupo como padrao produtivo

O framework deve reduzir o custo de trabalhar em grupo:

- `GROUP.md` identifica membros e responsabilidades.
- `SPLIT.md` define partes, branches e interfaces.
- Cada membro pode pedir à IA: “faça minha parte”, “revise a parte de X”, “assuma a parte Y” ou “integre tudo”.
- O padrao Git recomendado é repo central + branch por membro/parte + Pull Request para `main`.
- A integração final deve seguir `INTEGRATION.md`, não improviso no fim.

## Protocolo de trabalho spec-driven e portal-first

1. **Contexto** — Ler `TASK_REGISTRY.md`, `GROUP.md` e `LOCAL.md` se existir.
2. **Fonte oficial** — Capturar URL/pagina do portal FIAP por `agent-browser` quando possível; se falhar, usar `FIAP_TASK_CAPTURE_TEMPLATE.md`.
3. **Tipo de entrega** — Classificar com [`docs/templates/FIAP_DELIVERY_TYPES.md`](templates/FIAP_DELIVERY_TYPES.md).
4. **Modo da task** — Perguntar se é solo ou grupo. Se grupo, perguntar se o aluno vai coordenar, fazer sua parte, revisar, assumir parte de alguém ou integrar.
5. **Intake** — Task nova: checklist, entregáveis, dúvidas ao aluno; registrar no registry.
6. **Spec** — Criar `specs/taskNN_nome/SPEC.md` antes de executar.
7. **Split/Plano** — Para grupo, criar `SPLIT.md` e `INTEGRATION.md`; sempre criar `WORKPLAN.md`.
8. **Execução** — Implementar apenas o escopo aprovado.
9. **Defesa e estudo** — Gerar perguntas de defesa e study pack quando ajudar prova, vídeo ou apresentação.
10. **Quality gate** — Testes/scripts que fizerem sentido; conferir `REVIEW.md`; atualizar registry.
11. **Segurança** — Conferir [`docs/templates/SAFETY_PII_COPYRIGHT_CHECKLIST.md`](templates/SAFETY_PII_COPYRIGHT_CHECKLIST.md) antes de publicar/exportar.
12. **Empacotamento** — ZIP, vídeo, portal; marcar **CONCLUÍDA** no registry.
13. **Retrospectiva** — O que funcionou / melhorar; sugerir atualização de documentação ou regras.

Workflows detalhados ficam em [`docs/workflows/`](workflows/).

## Como o aluno inicia fluxos

O framework deve aceitar entradas naturais no chat:

- **Task/challenge colada no chat:** a IA processa o enunciado completo, pergunta solo/grupo e cria os arquivos em `specs/` antes da execução.
- **Task por URL do portal:** a IA segue [`docs/workflows/09-task-portal-first.md`](workflows/09-task-portal-first.md), captura fonte oficial e preserva rubrica, prazo e anexos.
- **Parte de task em grupo:** a IA usa `GROUP.md`, `LOCAL.md` e `SPLIT.md` para limitar o trabalho à responsabilidade do aluno.
- **PDF de aula:** a IA extrai o conteúdo e salva pílula + flashcards em `knowledge/`.
- **Texto copiado de página da aula:** a IA trata o texto colado como fonte de aula, limpa ruído de navegação e gera material de estudo.
- **Estudo para prova/defesa:** a IA gera study pack com Cornell, Feynman, quiz bank, mapa conceitual, defesa oral e SRS.

Prompts prontos ficam no [`README.md`](../README.md) e em [`SETUP.md`](../SETUP.md).

## Profundidade do assistente (qualquer produto)

- **Trabalho corrente** — edições, testes, pequenos passos, registry, gerar pílulas a partir de texto colado.
- **Momentos mais exigentes** — intake de enunciado grande, arquitetura, revisão pré-entrega, debug difícil, simulação de prova.

Regra prática: começar pelo fluxo simples; se falhar duas vezes no mesmo bloqueio, aumentar o nível de análise (modelo mais capaz ou sessão mais longa), conforme o que o IDE oferecer.

## Integração opcional com o portal FIAP

Ver [integrations/fiap-portal-helper.md](integrations/fiap-portal-helper.md) — extração de conteúdo para `knowledge/`, **sem** submissão automática de avaliações e **sem** credenciais no Git.

## Integrações opcionais de estudo e automação

- NotebookLM comum: exportar pacote seguro e importar manualmente via Drive.
- NotebookLM Enterprise/API: usar somente quando houver ambiente Google Cloud e politica de dados definida.
- CLI-Anything: experimental, nunca obrigatório, e não deve substituir o fluxo portal-first.

## Padrões globais

- Comentários e docs ao aluno: **pt-BR**; identificadores de código em **inglês** (`snake_case` em Python, `camelCase` em JS/TS).
- Não instalar dependências externas sem alinhar com o Product Owner.
- Código limpo, sem comentários que só repetem o código.

## Referência rápida

| Tarefa | Prioridade |
|--------|------------|
| Ler `TASK_REGISTRY.md` | Sempre primeiro |
| Ler `GROUP.md` (grupo + colegas) | Em seguida |
| Ler `LOCAL.md` se existir (quem está neste clone) | Depois do grupo |
| Intake / arquitetura / revisão final | Assistente (chat) |
| Implementação / terminal | Assistente, com confirmação do aluno para efeitos colaterais |
| Atualizar `TASK_REGISTRY.md` | Quem concluiu a alteração de estado |
| Atualizar dashboards | Hook do Cursor ou `python scripts/update_workflow_dashboard.py --quiet` |

Integração humana do grupo: [`SETUP.md`](../SETUP.md).

## Cursor (opcional)

Quem usa **Cursor** pode ainda beneficiar de [`.cursor/rules/`](../.cursor/rules/) (regras extra por tópico). O contrato mínimo continua a ser este `FRAMEWORK.md` + `TASK_REGISTRY.md` + `GROUP.md` (+ `LOCAL.md` se existir).
