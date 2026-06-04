# Dicionário de Dados — AgroKraken Sprint 2

**Autor:** Higor Henrique Garcia (RM571820)  
**Arquivo:** `data/dataset_simulado.csv`  
**Destino SQL:** tabela `operacoes` em `data/agrokraken.db`

## Visão geral

Dataset simulado de operações de equipamentos agrícolas (tratores, colheitadeiras, plantadeiras) em condições de campo e transporte. Cada linha representa uma operação com telemetria de sensores e variáveis ambientais, alinhada à User Story da persona **Carlos (operador)** e ao escopo Sprint 1.

**Geração:** `python scripts/generate_dataset.py` (seed=42, ≥600 linhas)  
**Ingestão:** `python scripts/ingest_data.py`

## Colunas (16)

| # | Coluna | Tipo | Unidade | Descrição | Faixa típica |
|---|--------|------|---------|-----------|--------------|
| 1 | `data_hora` | datetime | — | Momento da operação | Mar–Mai/2026 |
| 2 | `equipamento_id` | string | — | Identificador do equipamento | TRAT-00x, COLH-00x, PLAN-00x |
| 3 | `tipo_operacao` | string | — | Contexto operacional | `campo`, `transporte` |
| 4 | `cultura` | string | — | Cultura no talhão | `soja`, `milho`, `cana` |
| 5 | `umidade_solo` | float | % | Umidade do solo medida in loco | 30–95 |
| 6 | `precipitacao_24h` | float | mm | Chuva acumulada nas últimas 24 h | 0–65 |
| 7 | `precipitacao_prevista` | float | mm | Previsão de chuva para próximas horas | 0–15 |
| 8 | `temperatura` | float | °C | Temperatura ambiente | 22–34 |
| 9 | `declividade_terreno` | float | % | Inclinação do terreno | 1.5–20 |
| 10 | `distancia_corpo_dagua` | float | m | Distância até rio/córrego/represa | 30–700 |
| 11 | `tipo_solo` | string | — | Classificação pedológica | `latossolo`, `argissolo`, `gleissolo` |
| 12 | `historico_sinistros_area` | int | count | Sinistros na área nos últimos 12 meses | 0–5 |
| 13 | `horas_uso_equipamento` | float | h | Horímetro acumulado do equipamento | 150–2100+ |
| 14 | `ultima_manutencao_dias` | int | dias | Dias desde última manutenção preventiva | 5–95 |
| 15 | `velocidade_vento` | float | km/h | Velocidade do vento no momento | 4–28 |
| 16 | `risco_label` | int | 0/1 | **Target ML:** 1 = risco alto, 0 = risco baixo | 0 ou 1 |

## Regras de risco (geração do label)

O `risco_label` é derivado de um score interno (0–100) com base em:

| Fator | Critério de alto impacto |
|-------|--------------------------|
| Proximidade da água | < 50 m (crítico), 50–200 m (alto) |
| Umidade do solo | > 85% (encharcado → atolamento) |
| Precipitação | > 40 mm/24h ou previsão > 8 mm |
| Declividade | > 15% (terreno íngreme) |
| Tipo de solo | `gleissolo` > `argissolo` > `latossolo` |
| Histórico da área | ≥ 3 sinistros recentes |
| Operação | `transporte` + vento forte (> 20 km/h) |
| Manutenção | > 60 dias sem revisão |

**Threshold:** `risco_label = 1` quando score ≥ 55.

## Faixas de distância (Sprint 1 / enunciado FIAP)

| Distância | Nível de risco operacional |
|-----------|----------------------------|
| > 500 m | Baixo |
| 200–500 m | Médio |
| 50–200 m | Alto |
| < 50 m | Crítico |

## Schema SQLite (`operacoes`)

Definido em `scripts/ingest_data.py` (espelho de `sql/01_schema.sql` — Humberto):

```sql
CREATE TABLE operacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora TEXT NOT NULL,
    equipamento_id TEXT NOT NULL,
    -- ... demais colunas iguais ao CSV
    risco_label INTEGER NOT NULL
);
```

Índices: `equipamento_id`, `risco_label`, `data_hora`.

## Contrato com outras partes

| Consumidor | Uso |
|------------|-----|
| Humberto (SQL) | Queries sobre `operacoes`; schema em `sql/01_schema.sql` |
| Vinicius (ML) | Features numéricas + `risco_label` para Random Forest |
| Igor (Dashboard) | Leitura via pipeline ou CSV para scores e alertas |

## Equipamentos simulados

| ID | Tipo implícito |
|----|----------------|
| TRAT-001 … TRAT-005 | Trator |
| COLH-001, COLH-003, COLH-005 | Colheitadeira |
| PLAN-001, PLAN-002 | Plantadeira |
