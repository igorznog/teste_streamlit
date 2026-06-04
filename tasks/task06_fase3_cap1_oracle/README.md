# FarmTech Solutions — Fase 3 Cap 1

> **Projeto Fase 3 — Etapas de uma Máquina Agrícola**
> PBL (Project-Based Learning) do curso de Inteligência Artificial — FIAP.
> Entrega-agregadora da Fase 3 (Banco de Dados Oracle + Dashboard + ML).

| Campo | Valor |
|-------|-------|
| **Disciplina** | Fase 3 — Colheita de Dados e Insights (1TIAOA) |
| **Grupo** | Vinicius Anjos (RM572814), Higor Henrique Garcia (RM571820), Igor (RM572822), Humberto (RM570536) |
| **Cultura** | Café (*Coffea arabica*) — continuidade da Fase 2 |
| **Prazo** | 19/05/2026 23h59 |
| **Vídeo demonstrativo** | [YouTube - Assista ao Vídeo](https://www.youtube.com/watch?v=_6Lw-zrImlQ) |

## 1. Visão geral da entrega

Cobrimos **as três frentes** da atividade para somar até **20 pts**:

| Frente | Pontos | Pasta | Status |
|--------|-------:|-------|--------|
| **Obrigatória** — Banco de Dados Oracle (carga dos dados Fase 2) | 10 | `sql/`, `dados/`, `prints/` | em execução |
| **Ir Além Op. 1** — Dashboard Python (Streamlit) | +5 | `dashboard/` | em execução |
| **Ir Além Op. 2** — ML no Agronegócio (notebook do Cap 10) | +5 | `ml/` | pronto (Cap 10) |

## 2. Estrutura do repositório

```
farmtech-fase3-cap1/
├── README.md                   <- este arquivo
├── MANUAL_ENTREGA.md           <- passo-a-passo + roteiro do vídeo
├── link_video.txt              <- URL YouTube não-listado
├── sql/
│   ├── 01_criar_tabela.sql     <- DDL idempotente
│   ├── 02_importar_csv.md      <- wizard Importar Dados (passos + prints)
│   └── 03_consultas.sql        <- 10 queries demonstrativas
├── dados/
│   ├── gerar_dataset.py        <- gera dataset determinístico (seed=42)
│   └── leituras_sensores.csv   <- 1000 leituras (timestamp,n,p,k,ph,umidade,bomba)
├── dashboard/
│   ├── app.py                  <- Streamlit app
│   ├── requirements.txt
│   └── README.md
├── ml/
│   ├── HigorHenriqueGarcia_RM571820_fase3_cap10.ipynb
│   ├── produtos_agricolas.csv
│   └── README.md
├── prints/                     <- screenshots Oracle SQL Developer + dashboard
├── docs/
│   └── INSTALAR_ORACLE_SQL_DEVELOPER.md
└── (.gitignore)
```

## 3. Frente obrigatória — Banco Oracle (10 pts)

### Dados de origem (Fase 2)

O ESP32 simulado no Wokwi monitora N, P, K, pH e umidade do solo de uma plantação de café.
O sketch C/C++ original está em [`tasks/imported/task3_farmtech_fase2/esp32/sketch.ino`](../imported/task3_farmtech_fase2/esp32/sketch.ino).

Schema (mesmo da Fase 2):

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `timestamp` | TIMESTAMP | Momento da leitura |
| `n`, `p`, `k` | NUMBER(1) | Presença de Nitrogênio / Fósforo / Potássio (0 ou 1) |
| `ph` | NUMBER(4,2) | pH do solo (0–14, café ideal 5.5–6.5) |
| `umidade` | NUMBER(5,2) | Umidade % (0–100, café ideal 60–80) |
| `bomba` | NUMBER(1) | Estado da bomba após a regra de irrigação (0 ou 1) |

### Geração reprodutível do CSV

```bash
python3 dados/gerar_dataset.py            # 1000 leituras, seed=42 (default)
python3 dados/gerar_dataset.py --linhas 5000  # se quiser mais
```

A função `decidir_bomba()` implementa a mesma lógica do `sketch.ino` da Fase 2
(faixa de pH 5.0–7.0, umidade alvo 60–80, chuva suspende bomba).

### Carga no Oracle

Passo-a-passo completo em [`sql/02_importar_csv.md`](sql/02_importar_csv.md).
DDL idempotente em [`sql/01_criar_tabela.sql`](sql/01_criar_tabela.sql).

Resumo:

1. Instalar Oracle SQL Developer ([`docs/INSTALAR_ORACLE_SQL_DEVELOPER.md`](docs/INSTALAR_ORACLE_SQL_DEVELOPER.md)).
2. Conectar em `oracle.fiap.com.br:1521/ORCL` com usuário `RM571820`.
3. Clicar com botão direito em **Tabelas (Filtrado)** → **Importar Dados…**.
4. Apontar para `dados/leituras_sensores.csv`, definir tipos da tabela.
5. Finalizar — 1000 linhas importadas.

### Consultas SQL (10 queries em [`sql/03_consultas.sql`](sql/03_consultas.sql))

| # | Query | Para que serve |
|---|-------|----------------|
| Q1 | `SELECT * FETCH FIRST 10 ROWS ONLY` | Conferência inicial |
| Q2 | `COUNT(*)` | Validar que vieram 1000 linhas |
| Q3 | min/max/avg/stddev de pH e umidade | Estatísticas descritivas |
| Q4 | `% de tempo com bomba ligada` | Eficiência da irrigação |
| Q5 | Soma de N, P, K | Qual nutriente é mais frequente |
| Q6 | pH e umidade médios **por hora do dia** | Perfil diário |
| Q7 | Leituras com pH fora de 5.5–6.5 | Alertas |
| Q8 | Solo seco (< 50%) com bomba desligada | Alertas críticos |
| Q9 | Quantos eventos de irrigação (transições 0→1) | Frequência de operação |
| Q10 | Top 5 janelas de 1h com pior umidade média | Períodos críticos |

## 4. Ir Além Opção 1 — Dashboard Streamlit (+5 pts)

```bash
cd dashboard
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
# abre em http://localhost:8501
```

Funcionalidades:

- 5 métricas no topo (leituras, umidade atual, pH atual, NPK presente, % bomba média).
- **Sugestão de irrigação em tempo real** (mesma lógica do ESP32).
- Filtro temporal via slider.
- 4 abas: Umidade & pH (com faixa ideal sombreada), NPK, Bomba (por hora + eventos), Tabela com download CSV.
- Toggle "chuva prevista" muda a sugestão (igual ao Opcional 1 do OpenWeather da Fase 2).

Detalhes em [`dashboard/README.md`](dashboard/README.md).

## 5. Ir Além Opção 2 — ML no Agronegócio (+5 pts)

Notebook do **Cap 10** já entregue, reaproveitado aqui como Opção 2. Cobre:

- Análise exploratória com ≥5 gráficos.
- 3 culturas comparadas (perfil ideal de solo/clima).
- 5 modelos preditivos distintos (Logistic Regression, KNN, Decision Tree, Random Forest, SVM).
- Avaliação comparativa (accuracy, confusion matrix, classification report).

Detalhes em [`ml/README.md`](ml/README.md).

## 6. Vídeo demonstrativo

Roteiro completo + tempos sugeridos em [`MANUAL_ENTREGA.md`](MANUAL_ENTREGA.md).
Subir como **"Não listado"** no YouTube. Colar a URL em `link_video.txt`.

## 7. Como conferir o trabalho

```bash
# 1. Dataset
python3 dados/gerar_dataset.py
head dados/leituras_sensores.csv

# 2. Dashboard
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py

# 3. Notebook ML
jupyter notebook ml/HigorHenriqueGarcia_RM571820_fase3_cap10.ipynb
```

A frente Oracle exige tela do SQL Developer; os prints em `prints/` são a evidência.

## 8. Autoria e crédito

Squad oriundo da Fase 2 (cultura: café) + Cap 10 (modelagem). Grupo no portal da FIAP:
**Vinicius Anjos, Higor Henrique Garcia, Igor, Humberto.**

Coordenação técnica e documentação: Higor Henrique Garcia
