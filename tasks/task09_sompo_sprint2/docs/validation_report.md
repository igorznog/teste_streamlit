# Relatório de Validação — ML AgroKraken Sprint 2

**Responsável:** Vinicius Anjos (RM572814)  
**Modelo:** Random Forest para score de risco operacional  
**Data da validação:** 04/06/2026  
**Dataset:** `data/dataset_simulado.csv`

## Resumo executivo

O modelo atingiu **recall de 96,30%** para a classe `risco_label=1`, usando threshold de alerta `0.34`. Como o objetivo do AgroKraken é prevenir sinistros, recall foi tratado como métrica principal: é melhor gerar alguns alertas preventivos a mais do que liberar uma operação realmente arriscada.

## Estratégia de validação

- Total de registros: 600
- Classe positiva (`risco_label=1`): 324 registros (54,0%)
- Split: 75% treino / 25% teste
- Treino: 450 registros
- Teste holdout: 150 registros
- Split estratificado por `risco_label`
- `random_state=42`

O threshold de validação foi definido como `0.34`, alinhado ao início da categoria `medio` no score 0–100. Portanto, scores a partir de 34 são tratados como alerta acionável para fins de recall.

## Métricas no conjunto de teste

| Métrica | Valor |
|---------|------:|
| Accuracy | 95,33% |
| Precision (`risco_label=1`) | 95,12% |
| Recall (`risco_label=1`) | 96,30% |
| F1-score (`risco_label=1`) | 95,71% |
| ROC AUC | 98,46% |

## Matriz de confusão

Labels: `0 = risco baixo`, `1 = risco alto`.

| Real \ Predito | Predito 0 | Predito 1 |
|----------------|----------:|----------:|
| Real 0 | 65 | 4 |
| Real 1 | 3 | 78 |

Interpretação:

- Verdadeiros positivos: 78 operações de risco alto corretamente alertadas.
- Falsos negativos: 3 operações de risco alto que não viraram alerta acionável.
- Falsos positivos: 4 operações de risco baixo sinalizadas como alerta acionável.
- O recall alto confirma aderência ao objetivo da Sprint 1: priorizar prevenção.

## Importância das variáveis

Top 10 features por importância do Random Forest:

| Feature | Importância |
|---------|------------:|
| `distancia_corpo_dagua` | 0,254039 |
| `tipo_solo_latossolo` | 0,227927 |
| `umidade_solo` | 0,129957 |
| `precipitacao_24h` | 0,096445 |
| `historico_sinistros_area` | 0,087786 |
| `tipo_solo_argissolo` | 0,044219 |
| `precipitacao_prevista` | 0,025910 |
| `tipo_solo_gleissolo` | 0,025895 |
| `declividade_terreno` | 0,021716 |
| `ultima_manutencao_dias` | 0,017760 |

A maior importância de distância até corpo d'água, tipo de solo, umidade e chuva é coerente com as regras de risco documentadas em `docs/data_dictionary.md`.

## Evidências geradas

Artefatos de validação:

- `models/risk_model_metrics.json`
- `models/feature_importance.csv`
- `models/risk_model.joblib`

Comando executado:

```bash
python ml/train_model.py --threshold 0.34
```

Teste rápido de predição:

```bash
python ml/predict.py --index 1
```

Saída observada:

```json
{
  "score": 96,
  "categoria": "alto",
  "tipo_risco": "proximidade alta de corpo d'água",
  "recomendacao": "Adiar a operação ou acionar a gestão antes de seguir; principal fator: proximidade alta de corpo d'água."
}
```

## Conclusão

O modelo atende ao contrato da Sprint 2: Random Forest treinado, score 0–100, categorias de risco, recomendação operacional e recall documentado. A validação indica bom desempenho no dataset simulado e deixa uma interface simples para integração com `dashboard/app.py` via `ml/predict.py`.
