# SPEC — Task 6 / Fase 3 Cap 1 — Banco de Dados Oracle (entrega agregadora)

> **Status:** APROVADA (escopo completo) — em execução.
> **Prazo de entrega:** terça-feira **19/05/2026 às 23h59** (≈ 2 dias e 3 horas em 17/05 20h).
> **Portal:** assign id=605373 — <https://on.fiap.com.br/mod/assign/view.php?id=605373&returnto=conteudocurso>
> **Enunciado fonte:** `docs/validation/captures/fases/fase3/tasks/task01_*/enunciado.md` + `rubricas.csv`.

## 1. Contexto

A "Cap 1 – Etapas de uma Máquina Agrícola" é, na prática, a **entrega-agregadora da Fase 3**. Ela mistura conteúdo de **vários capítulos** num único PBL (Project-Based Learning) da FarmTech Solutions, e tem três frentes:

| Frente | Pontos | Conteúdo | Status atual |
|--------|--------|----------|--------------|
| **Obrigatória — Banco de Dados Oracle** | 10 | Carregar dados da Fase 2 no Oracle SQL Developer, prints, README, vídeo | NÃO INICIADA |
| **Ir Além Opção 1 — Dashboard Python** | +5 | Streamlit/Dash com umidade/P/K/pH/irrigação | NÃO INICIADA |
| **Ir Além Opção 2 — ML Agronegócio** | +5 | Análise + 5 modelos preditivos sobre `produtos_agricolas.csv` | **JÁ EXISTE** em `tasks/imported/task4_farmtech_ia_cap10/` (Task 4) |

A Opção 2 do "Ir Além" é **materialmente equivalente** ao que já foi entregue no Cap 10 (assign 605374). O notebook `HigorHenriqueGarcia_RM571820_fase3_cap10.ipynb` cumpre toda a rubrica (5 modelos, 3 culturas, avaliação comparativa).

## 2. Material já disponível

- **Dados de sensores Fase 2**: `tasks/imported/task3_farmtech_fase2/opcional2_analise/leituras_exemplo.csv`
  - Colunas: `timestamp, n, p, k, ph, umidade, bomba` (17 linhas de exemplo).
  - Origem: ESP32 simulado no Wokwi (cultura: café), squad WOLF, Fase 2.
- **Hardware Fase 2**: `tasks/imported/task3_farmtech_fase2/esp32/sketch.ino` + `diagram.json`.
- **Notebook ML (reaproveitar como Opção 2)**: `tasks/imported/task4_farmtech_ia_cap10/HigorHenriqueGarcia_RM571820_fase3_cap10.ipynb` + `produtos_agricolas.csv`.
- **Enunciado oficial completo**: capturado e parseado.
- **Rubricas estruturadas (3 baremas)**: `rubricas.csv`.

## 3. Rubricas (extraídas do portal)

### Obrigatória — Banco de Dados Oracle (10 pts)

| Critério | Pontos |
|---------|-------:|
| Organização do repositório GitHub | 2,0 |
| Documentação (README.md) com prints | 2,0 |
| Carga de dados no Oracle (com prints) | 2,0 |
| Consultas SQL corretas e funcionais | 2,0 |
| Vídeo demonstrativo (até 5 min) | 2,0 |
| **Total** | **10,0** |

### Ir Além Opção 1 — Dashboard Python (+5 pts)

| Critério | Pontos |
|---------|-------:|
| Funcionamento da Dashboard (≥3 variáveis: umidade, pH, P/K) | 1,5 |
| Interatividade/Visualização (Streamlit, Dash, etc.) | 1,0 |
| Integração com dados da Fase 2 | 1,0 |
| Documentação no GitHub | 0,5 |
| Vídeo demonstrativo (até 5 min) | 1,0 |
| **Total** | **5,0** |

### Ir Além Opção 2 — ML no Agronegócio (+5 pts)

| Critério | Pontos |
|---------|-------:|
| Análise exploratória (≥5 gráficos) | 1,0 |
| Discussão perfil ideal solo/clima (3 culturas) | 1,0 |
| Modelagem preditiva (5 modelos distintos) | 1,5 |
| Avaliação de performance | 1,0 |
| Documentação e Notebook | 0,5 |
| **Total** | **5,0** |

## 4. Estrutura proposta

```
tasks/task06_fase3_cap1_oracle/
├── README.md                  # documentação principal (rubrica obrigatória)
├── MANUAL_ENTREGA.md          # roteiro do vídeo + passo-a-passo de entrega
├── link_video.txt             # URL YouTube não-listado
├── sql/
│   ├── 01_criar_tabela.sql    # DDL da tabela de leituras
│   ├── 02_importar_csv.md     # passo-a-passo do wizard "Importar Dados"
│   └── 03_consultas.sql       # SELECT *, agregações, filtros
├── dados/
│   └── leituras_sensores.csv  # cópia do leituras_exemplo.csv (ou ampliada)
├── prints/                    # screenshots Oracle SQL Developer (passos 1..15)
│   ├── 01_conexao.png
│   ├── 02_importar.png
│   ├── ...
│   └── 15_select_all.png
└── (opcional) dashboard/
    └── app_streamlit.py       # só se Ir Além Opção 1 entrar no escopo
```

## 5. Cronograma sugerido (2 dias e 3 horas)

| Quando | O quê | Estimativa |
|--------|-------|-----------|
| Hoje 18/05 (D-1) noite | Decisões de escopo, criar repo GitHub, validar acesso Oracle | 1h |
| 18/05 manhã | Carga no Oracle + prints + DDL + SQL | 2-3h |
| 18/05 tarde | README + roteiro do vídeo | 2h |
| 19/05 manhã | Gravar e editar vídeo (até 5min) | 1-2h |
| 19/05 tarde | Push GitHub, submeter no portal, conferir entrega | 1h |
| 19/05 noite | Buffer / refinamento | 1h |

Se a Opção 1 (Dashboard) entrar, adicionar +3h em 18/05 manhã.
Se a Opção 2 (ML) entrar, é apenas anexar o notebook já pronto (+30min de README).

## 6. Decisões aprovadas (PO: Higor — 17/05/2026)

| # | Decisão | Escolha |
|---|---------|---------|
| 1 | **Escopo** | **TUDO** — Obrigatória (10) + Dashboard (+5) + ML (+5) = **20 pts potenciais** |
| 2 | **Grupo** | **Mesmo do Cap 10** (Vinicius, Igor, Humberto, Higor) via "Trazer Grupo Anterior" no portal |
| 3 | **Oracle SQL Developer** | **Não instalado ainda** → guia de instalação será parte da entrega (e do MANUAL_ENTREGA) |
| 4 | **GitHub** | **Repo novo** (`farmtech-fase3-cap1`) |
| 5 | **Vídeo** | **Higor grava e narra** (script ajuda em `MANUAL_ENTREGA.md`) |
| 6 | **Dados Oracle** | **Dataset expandido** (~1000 linhas) gerado por script determinístico, schema da Fase 2 |

## 7. Riscos e observações

- Portal aceita entrega **até 3 dias depois do prazo** com penalidade (até 70% da nota). Isso dá margem real até 22/05 — usar só como contingência.
- A senha Oracle DDMMYY pode estar bloqueada se ninguém usou no semestre — testar logo na instalação.
- O vídeo no YouTube deve ser configurado como **"não listado"** (instrução do enunciado).
- O notebook do Cap 10 será **anexado por referência** (link + cópia em `ml/`) — não precisa re-rodar.
- Dashboard Streamlit roda local na sua máquina; print + vídeo são suficientes para a rubrica.

## 8. Plano de execução (eu vs. você)

| Etapa | Quem | Status |
|-------|------|--------|
| Spec aprovada | PO | ✓ |
| Estrutura do projeto | IA | em andamento |
| Script gerador de dados (1000 linhas, determinístico) | IA | em andamento |
| DDL Oracle + queries SQL | IA | em andamento |
| Wizard de importação (passo-a-passo com prints esperados) | IA | em andamento |
| Guia de instalação Oracle SQL Developer (Windows/WSL2) | IA | em andamento |
| Dashboard Streamlit (Opção 1) | IA | em andamento |
| Referência ao notebook Cap 10 (Opção 2) | IA | em andamento |
| README + MANUAL_ENTREGA + roteiro do vídeo | IA | em andamento |
| Instalar Oracle SQL Developer + testar login | **Você** | pendente |
| Rodar wizard de import + tirar prints | **Você** | pendente |
| Rodar dashboard local + tirar prints | **Você** | pendente |
| Gravar vídeo (até 5 min) | **Você** | pendente |
| Criar repo `farmtech-fase3-cap1` no GitHub + push | **Você** | pendente |
| Convidar grupo do Cap 10 no portal ("Trazer Grupo Anterior") | **Você** | pendente |
| Submeter `Entregar atividade` no portal | **Você** | pendente |
