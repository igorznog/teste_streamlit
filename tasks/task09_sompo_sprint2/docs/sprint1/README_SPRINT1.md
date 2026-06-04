# Sprint 1 — AgroKraken (importado)

> Snapshot importado do repo do Vinicius em 28/05/2026.  
> Fonte: https://github.com/vinialveslopesanjos/sompo-enterprise-challenge  
> Autor Sprint 1: Vinicius Alves Lopes dos Anjos (RM572814) — Grupo 68

## Vídeo

https://youtu.be/9uXrHvyAYXw

## Problema

Equipamentos agrícolas operam em condições variáveis (solo encharcado, terreno inclinado, proximidade de rios). Decisões reativas geram sinistros evitáveis para operadores, gestores e seguradora (Sompo).

## Solução — AgroKraken

Plataforma de análise preditiva de risco:

- Score 0–100 por operação
- Alertas: atolamento, colisão, superaquecimento, transporte
- Recomendações: adiar, mudar rota, reduzir carga
- Painel gestor + relatório seguradora

## Personas

1. **Carlos** — operador de campo (alerta simples no celular)
2. **Renata** — gestora de frota (visão preditiva diária)
3. **Marcos** — analista Sompo (histórico de scores vs sinistros)

## User Story principal (Sprint 2)

> Como **Carlos**, operador, quero receber um **alerta com score de risco** antes de iniciar a operação, com base em umidade, chuva, declividade, distância da água e histórico da área.

## Variáveis (dataset)

Ver tabela completa no README original — colunas: `data_hora`, `equipamento_id`, `tipo_operacao`, `cultura`, `umidade_solo`, `precipitacao_24h`, `precipitacao_prevista`, `temperatura`, `declividade_terreno`, `distancia_corpo_dagua`, `tipo_solo`, `historico_sinistros_area`, `horas_uso_equipamento`, `ultima_manutencao_dias`, `velocidade_vento`, `risco_label`.

## Modelo proposto (Sprint 1)

- **Algoritmo:** Random Forest
- **Saída:** score 0–100; faixas baixo (0–33), médio (34–66), alto (67–100)
- **Métrica principal:** Recall

## Arquitetura (visão Sprint 1)

```
Sensores/APIs/Histórico → Python/Pandas → Classifier (score 0-100)
    → App Operador | Painel Gestor | Relatório Sompo
```

## Sprint 2 prometida no README original

- Pipeline de dados simulados
- Treino inicial do modelo
- Banco SQL (PostgreSQL na visão longo prazo; SQLite na Sprint 2)
- Protótipo dashboard operador
