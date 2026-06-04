# Dashboard FarmTech (Streamlit) — Ir Além Opção 1 (+5 pts)

Dashboard interativo que lê o CSV gerado pela Fase 2 (`dados/leituras_sensores.csv`)
e mostra umidade, pH, NPK, estado da bomba e sugestão de irrigação ao vivo.

## Como rodar

```bash
cd dashboard
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Abrir <http://localhost:8501> no navegador.

## O que mostra (cobre a rubrica)

| Critério da rubrica (5 pts) | Onde |
|----|------|
| Funcionamento da Dashboard (≥3 variáveis) — 1,5 | métricas + aba "Umidade & pH" + aba "NPK" |
| Interatividade Streamlit — 1,0 | sidebar com filtros (CSV, chuva prevista), slider de janela temporal, abas |
| Integração com dados da Fase 2 — 1,0 | usa `leituras_sensores.csv` (mesmo schema do CSV da Fase 2) |
| Documentação no GitHub — 0,5 | este README + comentários no código |
| Vídeo demonstrativo até 5min — 1,0 | gravado pelo Higor (ver `MANUAL_ENTREGA.md` para roteiro) |

## Prints sugeridos para o README principal

- `prints/dash_01_home.png` — visão geral com métricas no topo.
- `prints/dash_02_umidade_ph.png` — gráfico de umidade + pH.
- `prints/dash_03_npk.png` — barras com presença de NPK.
- `prints/dash_04_bomba_por_hora.png` — bomba por hora.
- `prints/dash_05_chuva_prevista.png` — sugestão muda ao marcar "chuva prevista" na sidebar.
