# Task Registry

> Memória persistente deste clone do `fiap-academic-workflow`. Toda sessão deve ler este arquivo primeiro, depois `GROUP.md` e `LOCAL.md` se existir.

## Status do Workspace

- **Workflow atual:** `fiap-academic-workflow` clonado em `~/fiap-academic-workflow`.
- **Origem do contexto migrado:** `~/fiap_squad_deliverables`.
- **Objetivo:** validar o novo fluxo spec-driven mantendo histórico suficiente do workflow WOLF antigo para próximas entregas FIAP.

---

## Task 1 — FarmTech Agricultura Digital
- **Status:** IMPORTADA / HISTÓRICA
- **Pasta:** `tasks/imported/task1_farmtech/`
- **Disciplina:** Agricultura Digital + Formação Social
- **Modo:** SOLO

### Contexto importado
- Entrega com CLI Python, cálculo de áreas, manejo de insumos, análise R e resumo/artigo.
- ZIP histórico copiado para `tasks/imported/task1_farmtech_WOLF.zip` quando presente.

### Uso no novo workflow
- Referência de estrutura de entrega solo.
- Pode virar exemplo futuro de `SPEC.md` + `WORKPLAN.md` se o grupo quiser documentar retrospectivamente.

---

## Task 2 — Teachable Machine: Utensílios de Cozinha
- **Status:** IMPORTADA / HISTÓRICA
- **Pasta:** `tasks/imported/task2_teachable_kitchen/`
- **Disciplina:** AI Challenges — Cap 2
- **Modo:** SOLO

### Contexto importado
- Scripts e materiais de relatório do desafio Teachable Machine.
- Knowledge relacionado em `knowledge/ai_challenges/`.

---

## Task 3 — FarmTech Fase 2: Sistema de Irrigação Inteligente
- **Status:** IMPORTADA / HISTÓRICA COM PENDÊNCIAS HUMANAS NO WORKFLOW ANTIGO
- **Pasta:** `tasks/imported/task3_farmtech_fase2/`
- **Disciplina:** Agricultura Digital — IoT / ESP32
- **Modo:** SOLO

### Pendências históricas registradas
1. Print do circuito Wokwi.
2. Vídeo final / link.
3. Push/submissão conforme portal.

### Uso no novo workflow
- Referência de task com hardware/simulação, documentação e opcionais.

---

## Task 4 — FarmTech IA Fase 3 Cap 10: Modelagem de IA
- **Status:** CONCLUÍDA — SUBMETIDA NO PORTAL EM 19/05/2026
- **Portal FIAP:** assign id=605374 — *Entrega concluída* em 19/05/2026
- **Portal URL:** <https://on.fiap.com.br/mod/assign/view.php?id=605374&returnto=conteudocurso>
- **Pasta:** `tasks/imported/task4_farmtech_ia_cap10/`
- **Spec sugerida:** `specs/imported/task4_farmtech_ia_cap10/SPEC.md`
- **Disciplina:** IA / Modelagem — análise exploratória + modelos preditivos
- **Prazo:** 19/05/2026 23h59
- **Modo:** GRUPO

### Integrantes / RMs
- Vinicius Anjos — RM572814
- Higor Henrique Garcia — RM571820
- Igor — RM572822
- Humberto — RM570536

### Entregáveis importados
- Notebook final: `tasks/imported/task4_farmtech_ia_cap10/HigorHenriqueGarcia_RM571820_fase3_cap10.ipynb`
- Dataset: `tasks/imported/task4_farmtech_ia_cap10/produtos_agricolas.csv`
- Notebooks individuais e referência.
- Gráficos e script gerador quando presentes no workspace antigo.

### Pendências humanas
1. [x] **Submeter o notebook no portal FIAP** (botão "Entregar atividade" em assign id=605374) — concluído em 19/05/2026.
2. [x] Confirmar push do repositório de entrega quando a autenticação GitHub estiver resolvida.

---

## Task 5 — Validação do Novo Workflow FIAP
- **Status:** EM ANDAMENTO
- **Pasta:** `docs/validation/`
- **Spec:** `specs/imported/workflow_validation/SPEC.md`
- **Modo:** GRUPO / INFRA DE TRABALHO

### Checklist
- [x] Clonar `fiap-academic-workflow` na home.
- [x] Preencher `GROUP.md` e `LOCAL.md`.
- [x] Migrar `knowledge/` do workflow antigo.
- [x] Migrar tasks históricas para `tasks/imported/`.
- [x] Preservar registry antigo em `docs/legacy/`.
- [x] Criar spec de validação do workflow.
- [x] Criar checklist para colegas testarem o fluxo.
- [x] Tornar obrigatória a autenticação inicial (Nome + RM) quando identidade do aluno estiver indefinida.
- [x] Padronizar mensagem de autenticação inicial para coleta de Nome + RM.
- [x] Criar skill de captura completa da FIAP (login assistido + Ctrl+C/Ctrl+V estruturado).
- [x] Implementar parser automático da captura FIAP para JSON/Markdown estruturado.
- [x] Implementar captura automática do portal FIAP (Playwright + sessão persistente) e skill portátil cross-IDE.
- [x] Adotar `vercel-labs/agent-browser` como engine preferencial cross-IDE (Cursor/Claude Code/Codex/etc.) com auth vault e fallback Playwright/manual.
- [x] Validar instalação real do `agent-browser 0.27.0` + Chrome 148 e snapshot do form de login da FIAP (`docs/validation/agent_browser_smoke_test.md`).
- [x] Criar `scripts/setup_fiap_automation.sh` (tudo-em-um, interativo, PT-BR) + `docs/QUICKSTART_AUTOMACAO.md` para onboarding rápido de novos alunos.
- [x] Validar auth login real e captura autenticada da Fase 3 (dashboard pessoal + 11 capítulos + 5 entregas detectados). Evidência em `docs/validation/agent_browser_smoke_test.md`.
- [x] Captura PDF-by-default de todas as fases liberadas (Fase 1: 9, Fase 2: 11, Fase 3: 12 = 32 PDFs / ~32 MB). Fase 4 detectada como não liberada. Script `scripts/fiap_capture_all_phases.py` com flags `--slides`, `--assets`, `--no-pdf`, `--phases`, `--max-chapters`, `--keep-output`. Evidência em `docs/validation/fiap_pdfs_captured.md`.
- [x] Criar onboarding guiado para colegas em `docs/workflows/00-onboarding-colega.md` e atualizar `README.md`/`SETUP.md`.
- [x] Criar matriz de tipos de entrega FIAP em `docs/templates/FIAP_DELIVERY_TYPES.md` e conectar ao intake/framework.
- [x] Documentar workflow portal-first em `docs/workflows/09-task-portal-first.md`.
- [x] Expandir estudo com templates Cornell, Feynman, mapa conceitual, quiz bank, defesa oral, SRS e workflow `docs/workflows/10-study-pack-generation.md`.
- [x] Adicionar export seguro para NotebookLM em `scripts/export_notebooklm_pack.py` + docs `docs/integrations/notebooklm.md`.
- [x] Documentar CLI-Anything como integração experimental em `docs/integrations/cli-anything.md`.
- [x] Adicionar checklist de segurança/PII/copyright em `docs/templates/SAFETY_PII_COPYRIGHT_CHECKLIST.md`.
- [x] Criar dashboards HTML estáticos para visão central, grupo, individual e registry em `docs/dashboard/`.
- [x] Criar gerador `scripts/update_workflow_dashboard.py` para atualizar os HTMLs a partir de `TASK_REGISTRY.md` e `GROUP.md`.
- [x] Adicionar modo silencioso/idempotente e hook Cursor para sincronizar dashboards após edições sem poluir o contexto dos agentes.
- [ ] Higor abrir o novo workspace no Cursor e iniciar uma conversa teste usando o prompt do README.
- [ ] Colegas clonarem/forkarem e validarem `GROUP.md`, `LOCAL.md`, task nova e split.

### Pendências do Higor
1. Abrir `~/fiap-academic-workflow` no Cursor como workspace principal de próximas tasks.
2. Rodar um teste real com uma próxima task ou aula.
3. Decidir se quer commitar/pushar os materiais migrados para o repo público ou manter parte deles só local.

---

## Task 6 — FarmTech Fase 3 Cap 1: Banco de Dados Oracle (entrega-agregadora)
- **Status:** EM ANDAMENTO — arcabouço técnico pronto, faltam ações humanas
- **Portal FIAP:** assign id=605373 — *Entrega pendente* até **terça 19/05/2026 23h59**
- **Portal URL:** <https://on.fiap.com.br/mod/assign/view.php?id=605373&returnto=conteudocurso>
- **Pasta:** `tasks/task06_fase3_cap1_oracle/`
- **Spec aprovada:** `specs/task06_fase3_cap1_oracle/SPEC.md`
- **Disciplina:** Fase 3 - Colheita de Dados e Insights
- **Prazo:** 19/05/2026 23h59 (≈ 2 dias e 3 horas restantes em 17/05 20h)
- **Modo:** GRUPO (reaproveitar grupo do Cap 10: Vinicius, Higor, Igor, Humberto)
- **Enunciado capturado:** `docs/validation/captures/fases/fase3/tasks/task01_*/enunciado.md` + `rubricas.csv` + `screenshot.png`

### Escopo aprovado (PO 17/05)
- **Obrigatória (10 pts)**: Banco Oracle (carga Fase 2 + 10 queries + prints + vídeo).
- **Ir Além Opção 1 (+5 pts)**: Dashboard Streamlit (umidade, pH, NPK, bomba).
- **Ir Além Opção 2 (+5 pts)**: notebook do Cap 10 reaproveitado em `ml/`.
- **Total potencial: 20 pts.**

### Entregáveis prontos (IA)
- `dados/gerar_dataset.py` + `dados/leituras_sensores.csv` (1000 linhas, seed=42).
- `sql/01_criar_tabela.sql` (DDL idempotente com constraints e índices).
- `sql/02_importar_csv.md` (wizard passo-a-passo com lista de prints).
- `sql/03_consultas.sql` (10 queries: estatísticas, alertas, perfil diário, eventos).
- `dashboard/app.py` + `requirements.txt` + `README.md` (Streamlit + Plotly, 5 métricas, 4 abas).
- `ml/` com notebook do Cap 10 copiado + `README.md` explicando dupla cobertura.
- `docs/INSTALAR_ORACLE_SQL_DEVELOPER.md` (Windows + WSL2 + troubleshooting).
- `README.md` principal + `MANUAL_ENTREGA.md` (roteiro de vídeo 4min30 detalhado).
- `link_video.txt` (placeholder), `.gitignore`.

### Progresso 17/05 ~21h (sem vídeo)
- [x] Dataset 1000 linhas + scripts SQL/DDL.
- [x] Dashboard Streamlit rodando + **5 prints** em `prints/dash_*.png`.
- [x] **6 prints SQL** locais (`sql_q3`, `q4`, `q6`, `q8`, `09_count`, `10_select`).
- [x] Notebook ML copiado em `ml/`.
- [x] Git local inicializado + commit em `tasks/task06_fase3_cap1_oracle/`.
- [x] `PREPARAR_ENTREGA.md` com checklist amanhã.
- [x] Carga real no Oracle FIAP (concluída via scripts em 19/05/2026).
- [ ] (Opcional) Prints wizard SQL Developer `01`–`08`. (Os prints da carga automática em `prints/oracle_auto/` cobrem isso)
- [ ] Vídeo YouTube + `link_video.txt`.
- [ ] `gh repo create` + push `farmtech-fase3-cap1`.
- [ ] Submeter Cap 10 e Cap 1 no portal.

### Pendências do Higor (amanhã — ver `PREPARAR_ENTREGA.md`)
1. **Oracle** (~20min): `export FIAP_ORACLE_PASSWORD='DDMMYY'` → `.venv/bin/python scripts/oracle_carga_fiap.py`.
2. **Vídeo** (~1h30): roteiro em `MANUAL_ENTREGA.md` bloco E.
3. **GitHub** (~15min): `gh auth login` + criar repo + push.
4. **Portal** (~15min): submeter Cap 10 + Cap 1 com links.

---

## Task 7 — Quiz Fase 3 - Colheita de Dados e Insights (individual)
- **Status:** NÃO INICIADA
- **Portal FIAP:** quiz id=605361 — *Pendente, máximo 1 tentativa* até **19/05/2026 23h59**
- **Portal URL:** <https://on.fiap.com.br/mod/quiz/view.php?id=605361&returnto=conteudocurso>
- **Modo:** INDIVIDUAL
- **Estratégia sugerida:** estudar pela `knowledge/fase3_overview/flashcards.md` + os 12 PDFs em `docs/validation/captures/fases/fase3/cap*/*.pdf` antes de iniciar (1 tentativa única, sem volta).
- **Enunciado capturado:** `docs/validation/captures/fases/fase3/tasks/task03_*/`

---

## Task 8 — Enterprise Challenge — SPRINT 1 — Sompo (grupo)
- **Status:** PRAZO ENCERRADO EM 29/04/2026 — verificar se houve submissão pelo grupo
- **Portal FIAP:** assign id=605883 — Higor consta como participante do grupo (visualizar apenas)
- **Portal URL:** <https://on.fiap.com.br/mod/assign/view.php?id=605883&returnto=conteudocurso>
- **Janela original:** 20/04/2026 a 29/04/2026
- **Modo:** GRUPO
- **Enunciado capturado:** `docs/validation/captures/fases/fase3/tasks/task04_*/`
- **Ação:** abrir o portal logado para conferir se há submissão registrada / nota / feedback.

---

## Task 9 — Enterprise Challenge — SPRINT 2 — Sompo (AgroKraken)
- **Status:** EM ANDAMENTO
- **Portal FIAP:** assign id=614389 — *Entrega pendente* até **04/06/2026 23h59**
- **Portal URL:** <https://on.fiap.com.br/mod/assign/view.php?id=614389&returnto=conteudocurso>
- **Janela:** 20/05/2026 a 04/06/2026
- **Modo:** GRUPO (4 integrantes — grupo novo; Sprint 1 do Vinicius importada como base)
- **Pasta execução:** `tasks/task09_sompo_sprint2/`
- **Spec:** `specs/task09_sompo_sprint2/SPEC.md` · `SPLIT.md` · `WORKPLAN.md` · `INTEGRATION.md`
- **Enunciado capturado:** `docs/validation/captures/fases/fase4/tasks/task04_enterprise_challenge_-_sprint_2_-_sompo/`
- **Sprint 1 (referência):** importada de <https://github.com/vinialveslopesanjos/sompo-enterprise-challenge> → `tasks/task09_sompo_sprint2/docs/sprint1/`

### Integrantes / divisão Sprint 2 (28/05/2026)
| Pessoa | RM | Branch | Parte |
|--------|-----|--------|-------|
| Higor Henrique Garcia | 571820 | `parte1-higor-dados` | Dados + EDA |
| Vinicius Anjos | 572814 | `parte4-vinicius-ml` | ML + validação |
| Igor | 572822 | `parte3-igor-dashboard` | Dashboard Streamlit |
| Humberto | 570536 | `parte2-humberto-integracao` | SQL + pipeline + entrega portal |

### Regra de repo
- **Desenvolvimento:** sempre neste monorepo `fiap-academic-workflow` (branches por pessoa).
- **Entrega Sompo (GitHub privado):** definida na empacotagem — ver `INTEGRATION.md`; não usar repo externo como fonte de verdade.

### Checklist
- [x] Importar base Sprint 1 (AgroKraken) para `tasks/task09_sompo_sprint2/`
- [x] SPEC + SPLIT + WORKPLAN + INTEGRATION
- [x] Grupo montado no portal FIAP (Grupo 58)
- [ ] Branches criadas pelos 4 integrantes
- [x] **P1 Higor:** dataset 600 linhas + `generate_dataset.py` + `ingest_data.py` + EDA + `data_dictionary.md`
- [ ] Pipeline dados → SQL → ML → dashboard
- [ ] Vídeo Sprint 2 + submissão assign 614389

---

## Knowledge Base

Materiais importados do workflow antigo:
- `knowledge/ai_challenges/`
- `knowledge/fase3_overview/`

---

## Histórico legado

- Registry antigo preservado em `docs/legacy/old_TASK_REGISTRY.md`.
- Plano antigo preservado em `docs/legacy/old_PLANO_DUAS_TASKS_24MAR.md`.

