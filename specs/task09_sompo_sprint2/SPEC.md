# SPEC — Task 9 — Enterprise Challenge Sprint 2 Sompo (AgroKraken)

> **Status:** EM ANDAMENTO — grupo novo, continuidade da Sprint 1 do Vinicius importada para o workflow.
> **Prazo:** quinta-feira **04/06/2026 23h59**
> **Portal:** assign id=614389 — <https://on.fiap.com.br/mod/assign/view.php?id=614389&returnto=conteudocurso>
> **Enunciado:** `docs/validation/captures/fases/fase4/tasks/task04_enterprise_challenge_-_sprint_2_-_sompo/`
> **Execução:** `tasks/task09_sompo_sprint2/`
> **Plano / split / integração:** `SPLIT.md`, `WORKPLAN.md`, `INTEGRATION.md`

## 1. Repositório central (regra do grupo)

- **Desenvolvimento, branches, PRs e histórico:** sempre neste clone — `fiap-academic-workflow`.
- **Pasta de execução:** `tasks/task09_sompo_sprint2/`.
- **Não** usar o repo externo do Vinicius como fonte de verdade; a Sprint 1 dele foi **importada** para `docs/sprint1/`.
- **Entrega no portal:** o enunciado pede GitHub privado. Na fase de empacotamento, o workflow define se espelha para repo de entrega ou se o tutor aceita subpath/documentação — ver `INTEGRATION.md` § Entrega.

## 2. Contexto

Grupo FIAP (Vinicius, Higor, Igor, Humberto) retoma o desafio Sompo. A Sprint 1 foi entregue pelo Vinicius isoladamente (**AgroKraken**, Grupo 68). O grupo atual precisa:

1. Manter **rastreabilidade** com a proposta Sprint 1 (personas, variáveis, Random Forest, score 0–100).
2. **Implementar** na Sprint 2: dados → SQL → ML → dashboard → validação → vídeo.

**Referência Sprint 1 importada:** repo original <https://github.com/vinialveslopesanjos/sompo-enterprise-challenge> (snapshot em `tasks/task09_sompo_sprint2/docs/sprint1/`).

## 3. Objetivo Sprint 2 (FIAP)

Integrar módulos de coleta/processamento, persistência SQL, modelo de ML supervisionado (score de risco 0–100), dashboard com alertas (operador + gestor) e documentação técnica — coerente com a User Story da persona **Carlos (operador)**.

## 4. Entregáveis obrigatórios (portal)

| # | Item | Pasta / artefato |
|---|------|------------------|
| 1 | Módulos integrados (coleta ↔ SQL ↔ ML ↔ UI) | `docs/architecture_v2.md`, `scripts/run_pipeline.py` |
| 2 | Scripts Python + queries SQL | `scripts/`, `sql/` |
| 3 | Relatório estatístico | `docs/validation_report.md` |
| 4 | Prints dashboard | `prints/` |
| 5 | Diagrama arquitetura | `docs/architecture_v2.md` |
| 6 | Documentação IA | `docs/ml_model.md` |
| 7 | README Sprint 2 + evolução Sprint 1 | `tasks/task09_sompo_sprint2/README.md` |
| 8 | Vídeo ≤ 5 min (não listado) | link em README |

## 5. Rotação de responsabilidades (acordado em 28/05/2026)

| Pessoa | RM | Parte |
|--------|-----|-------|
| Higor Henrique Garcia | 571820 | Dados + EDA (ex-Vinicius) |
| Vinicius Anjos | 572814 | ML + validação (ex-Humberto) |
| Humberto | 570536 | SQL + integração + entrega portal (ex-Higor) |
| Igor | 572822 | Dashboard Streamlit (inalterado) |

Detalhes: `SPLIT.md`.

## 6. Critérios de aceite (quality gate)

- [ ] Pipeline roda do zero: `generate` → `ingest` → `train` → `streamlit run dashboard/app.py`
- [ ] Dataset ≥ 500 linhas, schema igual ao README Sprint 1
- [ ] Modelo Random Forest + score 0–100 + faixas baixo/médio/alto
- [ ] Recall documentado (métrica principal Sprint 1)
- [ ] Dashboard: aba operador + aba gestora
- [ ] README com 4 integrantes e instruções de execução
- [ ] Vídeo no README; submissão portal assign 614389

## 7. Pendências humanas

1. Montar grupo no portal (Trazer Grupo Anterior / convites).
2. Definir na entrega se repo privado espelhado ou link do workflow (alinhar com tutora **nicollycrs**).
3. Gravar vídeo e submeter até 04/06.
