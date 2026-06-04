# Opcional 2 — Análise estatística em R

Script `irrigacao_stats.R` lê um CSV com leituras simuladas dos sensores e
recomenda se a bomba de irrigação deve ser **ligada** ou **desligada** para a
cultura do café.

## Execução

```bash
Rscript irrigacao_stats.R                      # usa leituras_exemplo.csv
Rscript irrigacao_stats.R outro_arquivo.csv    # usa outro CSV
```

Sem dependências externas — apenas R base.

## Estrutura do CSV esperado

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `timestamp` | string | Momento da leitura |
| `n`, `p`, `k` | 0/1 | Botões verdes pressionados |
| `ph` | float | pH simulado (0–14) |
| `umidade` | float | Umidade do solo (%) |
| `bomba` | 0/1 | Estado da bomba no momento da leitura |

## Regra de decisão implementada

1. Estatísticas descritivas (`mean`, `sd`) de `ph` e `umidade`.
2. **Teste t unilateral** (`H0: média da umidade >= 70%`).
3. Recomenda **LIGAR** se:
   - `p-valor < 0.05` (média significativamente abaixo de 70%); **e**
   - `pH médio` está na faixa do café (5.5–6.5).
4. Caso contrário, recomenda **DESLIGAR**.

## Saída

- Log completo no console (estatísticas, teste, recomendação).
- `graficos/boxplot_umidade_ph.png` — boxplots com as faixas ideais marcadas.
