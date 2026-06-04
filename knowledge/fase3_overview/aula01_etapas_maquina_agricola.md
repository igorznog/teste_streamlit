# Etapas de uma Máquina Agrícola (Fase 3 — Cap 01)
**Curso**: 1TIAOA | **Cap**: 01 — Overview da Fase 3 | **Material**: PDF FIAP

## Conceito-chave
A Fase 3 materializa o que veio antes: a FarmTech Solutions deixa de ser exercício de CLI e vira um **sistema físico de irrigação inteligente** com banco SQL e dados sendo analisados por estatística, R e ML. As 6 disciplinas da fase são engrenagens dessa "máquina agrícola".

## Como funciona — papel de cada disciplina
- **AI Challenges**: liga o mundo físico ao digital. Estuda **sensores** e **processamento de sinais** — representação no tempo/frequência, amostragem, reconstrução, e filtros (passa-baixa, passa-alta, passa-faixa, rejeita-faixa) para limpar ruído antes do dado virar entrada de IA.
- **Python (Numpy, Pandas, Matplotlib, Seaborn)**: Numpy para arrays e álgebra linear; Pandas para DataFrames (importar, limpar, agrupar, juntar); Matplotlib/Seaborn para visualização (gráficos categóricos, distribuições).
- **Statistical Computing with R**: análise de **clusters** — k-means e hierárquico — para achar padrões ocultos nos dados do agro.
- **Cognitive Data Science** (disciplina nova): **modelagem de banco de dados**. É o passo de armazenar antes de aplicar ML. Liga IoT (ESP32) → banco → análise.
- **Machine Learning & Modelling**: introdução ao **aprendizado supervisionado**, especialmente **classificação**. Aqui começam os modelos de verdade.
- **Formação Social**: tecnologia como ferramenta de **gestão estratégica**, sustentabilidade e uso eficiente de recursos hídricos/energéticos — tema que casa com irrigação.

## Pegadinhas de prova
- Cognitive Data Science **é nova** na Fase 3 — não confundir com Python ou R.
- A Fase 3 ainda **NÃO** implementa ML aplicado de verdade — só "introduz" classificação. ML aplicado vem nas próximas fases.
- O entregável central da fase é **sistema físico + banco SQL**, não dashboard nem app.
- Filtros de sinal (passa-baixa, passa-alta, passa-faixa, rejeita-faixa) → cobrados em AI Challenges, não em ML.
- Clusters em R = **não supervisionado** (k-means, hierárquico). Classificação em ML = **supervisionado**. Não trocar os termos.

## Conexões
- Continuação direta da Task 3 (`task3_farmtech_fase2/`) — ESP32 + sensores → agora com persistência em banco SQL.
- Pílulas relacionadas: `knowledge/ai_challenges/aula02b_lgpd_tipos_ia.md`, `knowledge/ai_challenges/aula02c_construindo_ia.md`.
