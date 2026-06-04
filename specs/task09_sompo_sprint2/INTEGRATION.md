# INTEGRATION — Task 9 Sompo Sprint 2

## Pipeline alvo

```
scripts/generate_dataset.py
        ↓
data/dataset_simulado.csv
        ↓
scripts/ingest_data.py  →  data/agrokraken.db (SQLite)
        ↓
ml/train_model.py       →  models/risk_model.joblib
        ↓
ml/predict.py           →  score 0-100 + recomendação
        ↓
dashboard/app.py        →  prints/ + demo vídeo
```

Comando único (Humberto entrega):

```bash
cd tasks/task09_sompo_sprint2
python scripts/run_pipeline.py
streamlit run dashboard/app.py
```

## Checklist de integração (03/06)

- [ ] Clone limpo do `fiap-academic-workflow` em máquina sem cache
- [ ] `pip install -r requirements.txt` na pasta da task
- [ ] Pipeline completo sem erro
- [ ] Dashboard exibe score para linha de teste conhecida
- [ ] README Sprint 2 atualizado (evolução Sprint 1 → 2)
- [ ] `docs/validation_report.md` com recall e matriz de confusão
- [ ] Prints em `prints/` referenciados no README

## Entrega portal (04/06)

| Campo | Valor |
|-------|--------|
| Assign | 614389 |
| URL | <https://on.fiap.com.br/mod/assign/view.php?id=614389> |
| Responsável submissão | Humberto |
| Vídeo | YouTube não listado, link no README |

### GitHub na entrega

O enunciado pede **repositório privado** compartilhado com **nicollycrs**.

**Desenvolvimento:** neste monorepo (`tasks/task09_sompo_sprint2/`).

**Na entrega**, uma destas opções (confirmar com tutora):

1. **Espelhar** `tasks/task09_sompo_sprint2/` para repo privado Sompo e submeter o link; ou  
2. **Submeter** link/documentação apontando para o path no workflow, se a tutora aceitar.

Registrar decisão final em `REVIEW.md` antes do submit.

## Dependências entre PRs

| PR | Bloqueia |
|----|----------|
| P1 dados | P2 ingest, P3 train |
| P2 SQL schema | P1 ingest (nomes de tabela) |
| P3 ML | P4 dashboard |
| P4 dashboard | Vídeo final |
| P2 pipeline | Entrega |
