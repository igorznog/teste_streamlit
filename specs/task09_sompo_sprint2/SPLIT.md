# SPLIT — Task 9 Sompo Sprint 2 (AgroKraken)

**Modo:** Grupo (4 integrantes)  
**Repo central:** `fiap-academic-workflow` (este clone)  
**Pasta de execução:** `tasks/task09_sompo_sprint2/`  
**Branch base:** `main`  
**Prazo:** 04/06/2026 23h59

## Papéis

| Papel | Pessoa | RM | Branch |
|-------|--------|-----|--------|
| Dados + EDA | Higor Henrique Garcia | 571820 | `parte1-higor-dados` |
| ML + validação | Vinicius Anjos | 572814 | `parte4-vinicius-ml` |
| SQL + integração + portal | Humberto | 570536 | `parte2-humberto-integracao` |
| Dashboard | Igor | 572822 | `parte3-igor-dashboard` |

## Partes

| Parte | Responsável | Arquivos / pastas | Saída esperada | Status |
|-------|-------------|-------------------|----------------|--------|
| P1 Dados | Higor | `data/`, `scripts/generate_dataset.py`, `scripts/ingest_data.py`, `notebooks/exploracao_inicial.ipynb`, `docs/data_dictionary.md` | CSV ≥500 linhas + ingestão SQLite | **Concluída (01/06)** |
| P2 SQL + pipeline | Humberto | `sql/`, `scripts/run_pipeline.py`, `docs/architecture_v2.md` | Schema, queries, pipeline integrado | Planejada |
| P3 ML | Vinicius | `ml/`, `models/`, `docs/validation_report.md`, `docs/ml_model.md` | RF + score 0–100 + métricas | Planejada |
| P4 Dashboard | Igor | `dashboard/app.py`, `prints/`, `requirements.txt` | Streamlit operador + gestora | Planejada |

## Ordem de merge

1. `parte1-higor-dados` — dataset + ingestão  
2. `parte2-humberto-integracao` — só SQL/schema  
3. `parte4-vinicius-ml` — modelo  
4. `parte3-igor-dashboard` — UI  
5. `parte2-humberto-integracao` — pipeline final, README Sprint 2, docs  

**Integrador / merge:** Humberto  
**Revisão:** rotativa (quem abre PR, outro revisa)

## Contrato entre partes

### CSV (Higor → todos)

Path fixo: `data/dataset_simulado.csv` — 16 colunas do README Sprint 1 §4.1.

### ML (Vinicius → Igor)

```python
# ml/predict.py
def predict_risk_score(row: dict) -> dict:
    return {
        "score": int,           # 0-100
        "categoria": str,       # baixo | medio | alto
        "tipo_risco": str,
        "recomendacao": str,
    }
```

### SQL (Humberto ↔ Higor)

Tabela `operacoes` — `ingest_data.py` grava colunas alinhadas ao schema em `sql/01_schema.sql`.

## Fluxo Git (cada dev)

```bash
cd ~/fiap-academic-workflow
git checkout main && git pull
git checkout -b parte1-higor-dados   # ou sua branch
# trabalhar só em tasks/task09_sompo_sprint2/
git add tasks/task09_sompo_sprint2/...
git commit -m "feat(sompo): ..."
git push -u origin parte1-higor-dados
# abrir PR → main no GitHub
```

## Regras

- Não commitar direto na `main`.
- Não editar pasta de outro na branch dele sem combinar.
- Commits com prefixo: `feat(sompo):`, `docs(sompo):`, `fix(sompo):`.
