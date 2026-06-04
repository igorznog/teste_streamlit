# Modelo de ML — AgroKraken Sprint 2

**Responsável:** Vinicius Anjos (RM572814)  
**Parte:** ML + validação  
**Data:** 04/06/2026  
**Arquivos principais:** `ml/train_model.py`, `ml/predict.py`, `models/risk_model.joblib`

## Objetivo

Treinar um modelo supervisionado para estimar o risco operacional de máquinas agrícolas antes da execução da atividade. A saída segue a proposta da Sprint 1 do AgroKraken: um **score de 0 a 100**, uma categoria (`baixo`, `medio`, `alto`), o principal tipo de risco e uma recomendação operacional para o Carlos (operador).

## Dados de entrada

Base utilizada: `data/dataset_simulado.csv`.

- Total de linhas: 600
- Target: `risco_label`
- Classe positiva: `1 = risco alto`
- Classe negativa: `0 = risco baixo`
- Proporção de risco alto: 324 registros (54,0%)

### Features usadas

Variáveis numéricas:

- `umidade_solo`
- `precipitacao_24h`
- `precipitacao_prevista`
- `temperatura`
- `declividade_terreno`
- `distancia_corpo_dagua`
- `historico_sinistros_area`
- `horas_uso_equipamento`
- `ultima_manutencao_dias`
- `velocidade_vento`

Variáveis categóricas:

- `tipo_operacao`
- `cultura`
- `tipo_solo`

As colunas `data_hora` e `equipamento_id` foram mantidas fora do treino para evitar que o modelo aprenda identificadores ou padrões temporais artificiais, em vez de fatores operacionais de risco.

## Algoritmo

O modelo final usa `RandomForestClassifier`, coerente com a proposta da Sprint 1.

Parâmetros principais:

- `n_estimators=350`
- `max_depth=8`
- `min_samples_leaf=2`
- `class_weight="balanced"`
- `random_state=42`

Pré-processamento:

- Numéricas: pass-through
- Categóricas: `OneHotEncoder(handle_unknown="ignore")`

O pipeline completo é salvo em `models/risk_model.joblib`, junto com as features esperadas, valores de fallback para predição e threshold de validação.

## Score e categorias

O score é calculado a partir da probabilidade estimada para `risco_label=1`:

```text
score = round(probabilidade_risco_alto * 100)
```

Faixas usadas no dashboard:

| Score | Categoria | Interpretação |
|-------|-----------|---------------|
| 0–33 | `baixo` | Operação liberada com monitoramento de rotina |
| 34–66 | `medio` | Operação exige cautela e monitoramento |
| 67–100 | `alto` | Recomenda-se adiar ou acionar a gestão |

Para validação binária, foi usado threshold `0.34`, alinhado ao começo da faixa `medio`. Assim, qualquer score a partir de 34 já conta como alerta acionável, o que prioriza recall e reduz o risco de deixar uma operação perigosa passar como segura.

## Contrato com dashboard

Arquivo: `ml/predict.py`

```python
from ml.predict import predict_risk_score

resultado = predict_risk_score(row)
```

Retorno:

```python
{
    "score": int,
    "categoria": "baixo | medio | alto",
    "tipo_risco": str,
    "recomendacao": str,
}
```

Exemplo de saída para uma operação de alto risco:

```json
{
  "score": 96,
  "categoria": "alto",
  "tipo_risco": "proximidade alta de corpo d'água",
  "recomendacao": "Adiar a operação ou acionar a gestão antes de seguir; principal fator: proximidade alta de corpo d'água."
}
```

## Como treinar

Na pasta `tasks/task09_sompo_sprint2/`:

```bash
python ml/train_model.py --threshold 0.34
```

Artefatos gerados:

- `models/risk_model.joblib`
- `models/risk_model_metrics.json`
- `models/feature_importance.csv`

## Como testar predição

```bash
python ml/predict.py --index 1
```

Também é possível passar uma linha em JSON:

```bash
python ml/predict.py --json-row '{"tipo_operacao":"campo","cultura":"soja","umidade_solo":88,"precipitacao_24h":45,"precipitacao_prevista":9,"temperatura":28,"declividade_terreno":12,"distancia_corpo_dagua":80,"tipo_solo":"gleissolo","historico_sinistros_area":3,"horas_uso_equipamento":1200,"ultima_manutencao_dias":70,"velocidade_vento":18}'
```

## Limitações

- A base é simulada, portanto o modelo ainda precisa ser revalidado com dados reais de sensores, clima e histórico de sinistros.
- O threshold foi escolhido no holdout local da Sprint 2, com foco em recall. Em produção, seria necessário acompanhar falsos positivos e recalibrar o score.
- A explicação `tipo_risco` usa regras heurísticas sobre a linha de entrada; ela não substitui técnicas de interpretabilidade, mas torna o alerta mais compreensível para o operador.
