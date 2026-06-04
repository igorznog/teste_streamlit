# AgroKraken — Sompo Enterprise Challenge

**FIAP IA 2026/1 — Turma 1TIAOA**  
**Task 9 — Sprint 2** (execução centralizada em `fiap-academic-workflow`)

| Integrante | RM | Parte Sprint 2 | Branch |
|------------|-----|----------------|--------|
| Higor Henrique Garcia | 571820 | Dados + EDA | `parte1-higor-dados` |
| Vinicius Anjos | 572814 | ML + validação | `parte4-vinicius-ml` |
| Igor | 572822 | Dashboard | `parte3-igor-dashboard` |
| Humberto | 570536 | SQL + integração + entrega | `parte2-humberto-integracao` |

**Spec / split / plano:** [`specs/task09_sompo_sprint2/`](../../specs/task09_sompo_sprint2/)  
**Prazo Sprint 2:** 04/06/2026 23h59 — [portal assign 614389](https://on.fiap.com.br/mod/assign/view.php?id=614389)

---

## Sprint 1 (base — importada do Vinicius)

Documentação completa: [`docs/sprint1/README_SPRINT1.md`](docs/sprint1/README_SPRINT1.md)  
Vídeo Sprint 1: https://youtu.be/9uXrHvyAYXw  
Origem externa (referência): https://github.com/vinialveslopesanjos/sompo-enterprise-challenge

**Resumo:** plataforma **AgroKraken** — score de risco 0–100, alertas preventivos, personas Carlos (operador), Renata (gestora), Marcos (Sompo). Modelo proposto: **Random Forest**, métrica principal **Recall**.

---

## Sprint 2 — estrutura do projeto

```
task09_sompo_sprint2/
├── README.md                 ← este arquivo
├── requirements.txt
├── data/
│   ├── dataset_simulado.csv
│   └── agrokraken.db         ← gerado na ingestão
├── sql/
├── scripts/
├── ml/
├── models/
├── dashboard/
├── notebooks/
├── docs/
├── prints/
└── link_video.txt            ← Sprint 2 (preencher)
```

---

## Como rodar (Parte 1 — Dados, Higor)

```bash
cd tasks/task09_sompo_sprint2
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Gerar dataset (600 linhas, seed=42)
python scripts/generate_dataset.py

# Ingerir no SQLite
python scripts/ingest_data.py

# EDA interativa
jupyter notebook notebooks/exploracao_inicial.ipynb
```

Dicionário de dados: [`docs/data_dictionary.md`](docs/data_dictionary.md)

---

## Como rodar (quando integrado)

```bash
cd tasks/task09_sompo_sprint2
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_pipeline.py
streamlit run dashboard/app.py
```

---

## Entregáveis Sprint 2

Ver checklist em [`specs/task09_sompo_sprint2/SPEC.md`](../../specs/task09_sompo_sprint2/SPEC.md).

---

*Desenvolvimento no monorepo `fiap-academic-workflow`. Repo privado de entrega Sompo — definido na fase de empacotamento (ver INTEGRATION.md).*
