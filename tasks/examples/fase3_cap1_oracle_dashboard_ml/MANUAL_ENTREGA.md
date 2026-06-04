# Manual de Entrega — Cap 1 / Fase 3

Passo-a-passo final para o **Aluno** rodar nas próximas 48h e submeter no portal.
Foco: o que **só você** consegue fazer (Oracle, prints, vídeo, GitHub, portal).

## Cronograma (até terça 19/05 23h59)

| Bloco | Quando | O quê | Tempo estimado |
|-------|--------|-------|---------------|
| A | Hoje noite (17/05) | Instalar SQL Developer + testar login Oracle | 30 min |
| B | Amanhã manhã (18/05) | Importar CSV + rodar SQLs + prints | 1h |
| C | Amanhã tarde (18/05) | Rodar dashboard + prints | 30 min |
| D | Amanhã noite (18/05) | Push repo GitHub | 30 min |
| E | Terça manhã (19/05) | Gravar vídeo (até 5min) + upload YouTube | 1h30 |
| F | Terça tarde (19/05) | Convidar grupo + submeter no portal | 15 min |
| G | Terça noite (19/05) | Buffer / contingência | livre |

**Total executivo: ~5h espalhados em 2 dias.**

---

## Bloco A — Oracle SQL Developer

1. Baixar e instalar SQL Developer 24.x **"with JDK 17"** seguindo
   [`docs/INSTALAR_ORACLE_SQL_DEVELOPER.md`](docs/INSTALAR_ORACLE_SQL_DEVELOPER.md).
2. Criar conexão `FIAP` (Host `oracle.fiap.com.br`, Porta `1521`, SID `ORCL`,
   Usuário `RM000000`, Senha DDMMYY).
3. Testar `SELECT USER, SYSDATE FROM dual;`.
4. **Print obrigatório**: `prints/00_conexao_ok.png` (árvore Conexões com FIAP verde).

> Se a senha não funcionar: chamado no helpcenter FIAP (pode demorar 1 dia útil — não procrastinar).

## Bloco B — Importar dados + SQL

Pré-requisito: dataset já gerado em `dados/leituras_sensores.csv` (1000 linhas).

1. Seguir [`sql/02_importar_csv.md`](sql/02_importar_csv.md) e tirar **10 prints**:
   - `prints/01_arvore_conexao.png`
   - `prints/02_importar_data_menu.png`
   - `prints/03_selecionar_arquivo.png`
   - `prints/04_nome_tabela.png`
   - `prints/05_colunas.png`
   - `prints/06_tipos_colunas.png`
   - `prints/07_preview.png`
   - `prints/08_concluido.png`
   - `prints/09_count_query.png`
   - `prints/10_select_all.png`
2. Rodar o `sql/03_consultas.sql` query por query e tirar prints das principais:
   - `prints/sql_q3_estatisticas.png`
   - `prints/sql_q4_bomba.png`
   - `prints/sql_q6_perfil_diario.png`
   - `prints/sql_q8_alertas.png`

> Atalho útil no SQL Developer: **Ctrl+Enter** executa a query do cursor.

## Bloco C — Dashboard

1. Abrir terminal na pasta `dashboard/`:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # ou .venv\Scripts\activate no PowerShell
   pip install -r requirements.txt
   streamlit run app.py
   ```

2. Abrir <http://localhost:8501> e tirar 5 prints:
   - `prints/dash_01_home.png` (visão geral com 5 métricas)
   - `prints/dash_02_umidade_ph.png` (gráfico tempo)
   - `prints/dash_03_npk.png` (barras NPK)
   - `prints/dash_04_bomba_por_hora.png`
   - `prints/dash_05_chuva_prevista.png` (sidebar com chuva marcada)

## Bloco D — Push GitHub

1. Criar repo público no GitHub: `farmtech-fase3-cap1`.
2. `cd tasks/task06_fase3_cap1_oracle && git init && git add -A`.
3. Commit `feat: entrega Cap 1 Fase 3 (Oracle + Dashboard + ML)`.
4. `git remote add origin git@github.com:<seu-user>/farmtech-fase3-cap1.git`.
5. `git push -u origin main`.
6. Atualizar este README com o link do repositório no topo.

> Lembre-se: o `.gitignore` do repo precisa ignorar `.venv/`, `__pycache__/`, etc.
> Os prints **devem** ser commitados (são a evidência da rubrica).

## Bloco E — Vídeo (até 5 minutos)

Roteiro abaixo. Tempo total ~4min30.

### 00:00–00:25 — Abertura

> "Olá, sou o Aluno Product Owner, RM000000. Aqui no projeto da Fase 3 Cap 1
> do curso de Inteligência Artificial da FIAP, fizemos a entrega-agregadora
> com o grupo: Aluno 2, Aluno 3, Aluno 4 e eu. O tema é a cultura de café
> usando os dados que coletamos da nossa máquina agrícola simulada na Fase 2.
> Cobrimos a entrega obrigatória (banco Oracle) e as duas opções de Ir Além
> (dashboard Python e modelagem de IA)."

### 00:25–01:30 — Banco de Dados Oracle (frente obrigatória)

- Mostrar SQL Developer aberto.
- Expandir árvore `FIAP` → `Tabelas (Filtrado)` → `LEITURAS_SENSORES`.
- Rodar `SELECT * FROM leituras_sensores FETCH FIRST 10 ROWS ONLY;`.
- Falar:
  > "Aqui está a tabela `LEITURAS_SENSORES` que importei pelo wizard a partir
  > do CSV gerado pela Fase 2 — 1000 linhas com timestamp, NPK, pH, umidade e
  > o estado da bomba para cada leitura do ESP32."
- Rodar `SELECT COUNT(*) FROM leituras_sensores;` (mostra 1000).
- Rodar Q3 (estatísticas) e Q4 (% bomba ligada):
  > "Olhando a estatística descritiva, o pH médio ficou em torno de 6.0, bem
  > dentro da faixa ideal do café, e a bomba ficou ligada em cerca de um terço
  > das leituras."

### 01:30–02:45 — Dashboard Streamlit

- Trocar para o navegador no <http://localhost:8501>.
- Mostrar as 5 métricas no topo.
- Mover o slider de janela temporal:
  > "O dashboard lê o mesmo CSV. Tenho 5 métricas no topo, uma sugestão de
  > irrigação em tempo real seguindo a lógica do sketch do ESP32, e quatro
  > abas com gráficos interativos."
- Trocar de aba: Umidade & pH → NPK → Bomba.
- Marcar checkbox "Chuva prevista" e mostrar a sugestão mudando.
- Voltar pra aba de tabela e clicar em "Baixar visualização atual".

### 02:45–04:00 — Modelagem de IA (Ir Além Opção 2)

- Abrir o notebook `ml/AlunoProductOwner_RM000000_fase3_cap10.ipynb`.
- Mostrar (rolagem rápida):
  - Cabeçalho com integrantes.
  - Gráfico exploratório (boxplot).
  - Tabela comparativa dos 5 modelos.
- Falar:
  > "Para a Opção 2 do Ir Além, anexamos o notebook do Cap 10 que o grupo já
  > tinha finalizado. São 5 modelos diferentes — regressão logística, KNN,
  > árvore de decisão, random forest e SVM — comparados em acurácia e matriz
  > de confusão para classificar a cultura recomendada com base no solo."

### 04:00–04:30 — Repositório e fechamento

- Mostrar o GitHub aberto na página do repositório.
- Mostrar a árvore de pastas (sql/, dados/, dashboard/, ml/, prints/, docs/).
- Falar:
  > "Tudo está organizado no repo `farmtech-fase3-cap1` com README documentando
  > cada frente, o passo-a-passo da carga no Oracle, os prints como evidência,
  > e os scripts para reproduzir o dataset, o dashboard e a análise. Valeu!"

### Configurações do vídeo

- Formato: 1080p ou 720p, **paisagem**.
- Plataforma: **YouTube como "Não listado"**.
- Não precisa edição sofisticada — uma gravação contínua de tela com microfone basta.
- Ferramentas sugeridas: OBS Studio (Windows) ou ShareX, ou Loom.
- Após upload, colar a URL em `link_video.txt`.

## Bloco F — Submissão no portal

1. Logar em <https://on.fiap.com.br/mod/EXEMPLO/view.php?id=000000>.
2. Clicar em **"Trazer Grupo Anterior"** na seção GRUPO (puxa Aluno 2/Aluno 3/Aluno 4).
3. Conferir que os 4 nomes aparecem na lista de participantes.
4. Clicar em **"Entregar Atividade"**.
5. Anexar:
   - Link do repositório GitHub.
   - Link do vídeo YouTube.
   - (opcional) ZIP do projeto caso queiram redundância.
6. Confirmar envio. Status muda de "Entrega pendente" para "Enviado para
   avaliação".
7. 📸 Print da confirmação → `prints/portal_entrega_confirmada.png`.

## Bloco G — Buffer

- Conferir que cada arquivo do repo abre sem erro.
- Conferir o vídeo no YouTube em modo anônimo (pra ver que está acessível com link).
- Tirar 5 min para revisar o README final como se fosse o professor avaliando.

## Checklist final

- [ ] SQL Developer instalado, conectado, 1000 linhas importadas, 10+ prints.
- [ ] Queries Q1–Q10 do `03_consultas.sql` rodadas; pelo menos 4 prints salvos.
- [ ] Dashboard rodando local, 5 prints salvos.
- [ ] Notebook ML no `ml/` abrindo sem erro.
- [ ] Repo GitHub `farmtech-fase3-cap1` público, README revisado, link no
      `link_video.txt`.
- [ ] Vídeo de até 5min publicado no YouTube como "Não listado".
- [ ] Grupo do Cap 10 reaproveitado no portal.
- [ ] **Atividade entregue no portal** (status muda no card da Cap 1).
- [ ] Print da confirmação salvo.
