# Task Registry

> Arquivo de rastreamento persistente. Qualquer modelo em qualquer conversa
> deve ler este arquivo para entender o estado atual do projeto.
> Atualizar sempre que um item mudar de status.

## Sprint 24/03/2026 — DUAS ENTREGAS NO MESMO DIA

**Task 1 (FarmTech)** e **Task 2 (Cap 2 / Teachable Machine)** com prazo **24/03/2026**.  
Plano único: **`PLANO_DUAS_TASKS_24MAR.md`** na raiz do repositório.

## Sprint 21/04/2026 — Task 3 FarmTech Fase 2

**Task 3 (FarmTech Fase 2 — IoT ESP32)** com prazo **21/04/2026 23h59**.

---

## Task 3 — FarmTech Fase 2: Sistema de Irrigação Inteligente (ESP32)
- **Status**: EM ANDAMENTO
- **Pasta**: `task3_farmtech_fase2/`
- **Disciplina**: Agricultura Digital — Fase 2 (IoT + Sensoriamento)
- **Prazo**: **21/04/2026 23h59**
- **Cultura escolhida**: Café (continuidade do Task 1)

### Checklist de Requisitos
- [x] (a) Circuito Wokwi.com com ESP32 — validado, rodando
- [x] (b) 3 chaves slide simulando N, P, K (true/false) — trocadas de pushbutton para slide por usabilidade; documentado no README
- [x] (c) Sensor LDR simulando pH (analógico, alterado manualmente junto com NPK)
- [x] (d) Sensor DHT22 simulando umidade do solo
- [x] (e) Relé azul como bomba d'água
- [x] (f) Lógica de decisão ligar/desligar bomba (NPK + pH + umidade + chuva)
- [x] (g) Justificativa agronômica completa para café (`docs/fundamentacao_agronomica.md`)
- [x] (h) Código C/C++ para ESP32 com diagnóstico por condição no Serial
- [x] (i) README.md completo com diagramas e lógica
- [ ] (j) Imagens do circuito Wokwi no README (aguardando print do Higor)
- [ ] (k) Repositório Git novo no GitHub (aguardando criação + push)
- [ ] (l) Vídeo YouTube ≤ 5 min, não listado
- [x] (ir além 1) Python + API OpenWeather → chuva suspende irrigação
- [x] (ir além 2) Análise estatística em R (teste t + boxplot)

### Entregáveis
- [x] `esp32/sketch.ino` — Código C/C++ ESP32
- [x] `esp32/diagram.json` — Diagrama Wokwi (board correto: `wokwi-esp32-devkit-v1`)
- [x] `esp32/wokwi.toml` — Config Wokwi
- [x] `esp32/libraries.txt` — Libs Arduino necessárias
- [x] `opcional1_openweather/clima.py` — Script OpenWeather
- [x] `opcional1_openweather/requirements.txt`
- [x] `opcional1_openweather/README.md`
- [x] `opcional2_analise/irrigacao_stats.R` — Análise R (validada localmente)
- [x] `opcional2_analise/leituras_exemplo.csv` — Dados simulados (25 pontos)
- [x] `opcional2_analise/README.md`
- [x] `docs/diagrama_logica.md` — Fluxograma + tabela verdade
- [x] `docs/fundamentacao_agronomica.md` — Embasamento científico
- [ ] `docs/circuito_wokwi.png` — Print do circuito (Higor gera)
- [x] `README.md` — Documentação principal
- [x] `MANUAL_ENTREGA.md` — Roteiro de vídeo + passo-a-passo
- [ ] `link_video.txt` — URL do vídeo (placeholder criado)

### Pendências Task 3 (só o Higor pode fazer)
1. **[AGORA]** Tirar print do circuito Wokwi com bomba LIGADA (`docs/circuito_wokwi.png`)
2. **[AGORA]** Gravar vídeo ≤ 5 min (roteiro em `MANUAL_ENTREGA.md`)
3. Postar no YouTube como "não listado" → colar URL em `link_video.txt`
4. Criar repo novo no GitHub (ex.: `farmtech-fase2`) e fazer push
5. Submeter link do repo na FIAP

### Aprendizados técnicos Task 3 (para retrospectiva)
- Wokwi: usar `wokwi-esp32-devkit-v1` (não `board-esp32-devkit-v1`)
- Wokwi: ESP32 precisa declarar `esp:TX0` / `esp:RX0` → `$serialMonitor` explicitamente
- Wokwi: slide switches resolvem problema de "segurar 3 botões" melhor que pushbuttons + alfinete
- LDR/pH: faixa 5.5-6.5 é estreita demais no slider → ampliamos para 5.0-7.0 (permitido pelo enunciado)

---

## Task 1 — FarmTech Agricultura Digital
- **Status**: EM ANDAMENTO
- **Pasta**: `task1_farmtech/`
- **Disciplina**: Agricultura Digital + Formação Social
- **Prazo**: **24/03/2026** (confirmar horário no portal FIAP)

### Checklist de Requisitos
- [x] (a) 2 culturas: Cana-de-açúcar e Café
- [x] (b) Cálculo de área: retângulo (cana) e círculo (café)
- [x] (c) Manejo de insumos: produto, dosagem/metro, ruas, comprimento → total litros
- [x] (d) Dados em vetores (listas de dicionários)
- [x] (e) Menu CLI: entrada, saída, atualização, deleção, sair
- [x] (f) Loop (while) e decisão (if/elif) com try/except
- [x] (g) R com estatísticas (média/desvio) dos dados exportados pelo Python
- [x] (h) Resumo do artigo Embrapa — PDF gerado via script Python (Arial 11, margens 2cm)
- [x] (ir além) API Open-Meteo em R com estatísticas

### Entregáveis
- [x] `main.py` — Menu CLI interativo
- [x] `culturas.py` — Lógica de CRUD, área e manejo
- [x] `estatistica.R` — Estatísticas dos dados da fazenda (lê CSVs)
- [x] `clima_estatistica.R` — API Open-Meteo (ir além)
- [x] `MANUAL_ENTREGA.md` — Manual com roteiro do vídeo
- [x] `resumo_artigo.txt` — Texto do resumo
- [x] `resumo_artigo.pdf` — Gerado (Arial 11, margens 2cm)
- [x] `link_video.txt` — FALTA link real do YouTube
- [x] Git inicializado com 3 commits
- [x] Repositório no GitHub (push — só se o enunciado exigir)
- [x] Vídeo gravado e postado no YouTube (não listado)
- [x] ZIP final gerado

### Pendências Task 1 (agora)
1. Gravar vídeo (~3–5 min) — roteiro resumido abaixo
2. YouTube → não listado → colar URL em `link_video.txt`
3. `zip -r task1_farmtech_WOLF.zip task1_farmtech/ ...` (comando na raiz do repo)
4. Upload na FIAP (ZIP + o que mais pedir)

---

## Task 2 — Teachable Machine: Utensílios de Cozinha (Cap 2)
- **Status**: CONCLUÍDA (entrega confirmada pelo Higor)
- **Pasta**: `task2_teachable_kitchen/`
- **Disciplina**: AI Challenges (Cap 2 — IA e seu mundo de possibilidades)
- **Aluno**: Higor Henrique Garcia | **RM**: 571820
- **Entrega**: `HigorHenriqueGarcia_RM571820_fase1_cap2.pdf`

### Checklist de Requisitos
- [x] (1a–c) Imagens por categoria; qualidade; treino vs teste
- [x] (2a–d) Teachable Machine; upload; parâmetros; treinos com Advanced
- [x] (3a–d) Testes e métricas
- [x] (4a) Relatório PDF completo

### Entregáveis
- [x] PDF entregue na FIAP

### Knowledge relacionado
- `knowledge/ai_challenges/aula02c_construindo_ia.md` (Teachable Machine, visão computacional)

---

## Task 4 — FarmTech IA 2026/1 | Fase 3 Cap 10 (Grupo 45 — notebooks)
- **Status**: EM ANDAMENTO (notebook final consolidado, executado e commitado localmente; push bloqueado por autenticação GitHub no terminal; submissão FIAP pendente)
- **Pasta:** `task_fiap_ia_fase3_grupo45/` (clone de [higorhg/fiap-ia-fase3-grupo45](https://github.com/higorhg/fiap-ia-fase3-grupo45))
- **Disciplina:** IA / Modelagem — análise exploratória + modelagem em `produtos_agricolas.csv`
- **Prazo:** 19/05/2026
- **Integrantes/RM:** Vinicius Anjos (RM572814), Higor Henrique Garcia (RM571820), Igor (RM572822), Humberto (RM570536)

### Checklist por parte
- [x] (1) Vinicius — Parte 1 integrada/completada no notebook final (gráficos 1–2)
- [x] (2) Higor — Parte 2: correlação, NPK boxplots, scatter T×umidade, achados (gráficos 3–5) — notebook `parte2_descritiva_HIGOR.ipynb`
- [x] (3) Igor — Parte 3 integrada a partir de `origin/parte3-igor` (perfil ideal + comparação de 3 culturas)
- [x] (4) Salim/Humberto — Parte 4 integrada a partir de `origin/humberto` (5 modelos + métricas + conclusões)
- [x] Notebook final consolidado: `HigorHenriqueGarcia_RM571820_fase3_cap10.ipynb` executado com sucesso via `jupyter nbconvert`

### Entregáveis / Git
- [ ] Branches `parte*-` integradas na `main` via Pull Request no repositório do grupo
- [x] Notebook final local com outputs e gráficos: `HigorHenriqueGarcia_RM571820_fase3_cap10.ipynb`
- [x] Gráficos exportados em `task_fiap_ia_fase3_grupo45/graficos/`
- [x] Script reprodutível: `gerar_notebook_final.py`
- [x] Commit local na `main` contendo apenas o notebook final: `6aa7d50 feat: add final cap10 notebook`
- [ ] Higor: autenticar GitHub no terminal e fazer `git push origin main`

### Pendências (Higor)
1. Revisar visualmente o notebook final executado antes de submeter.
2. Fazer commit/push do notebook final, `README.md`, `requirements.txt`, `.gitignore`, `gerar_notebook_final.py` e `graficos/` quando quiser versionar.
3. Submeter o notebook final na FIAP; se o portal também pedir vídeo, gravar até 5 min apresentando os principais gráficos e o melhor modelo.

---

## Task 5 — Framework FIAP clonável (`fiap-cursor-framework`)
- **Status**: CONCLUÍDA (estrutura + extensão IDE-agnóstica; push GitHub pendente)
- **Pasta:** `fiap-cursor-framework/`
- **Objetivo:** Repo neutro com `.cursorrules`, `.cursor/rules/`, `knowledge/`, `scripts/sync_knowledge.sh`, `TASK_REGISTRY.md` template, `docs/FRAMEWORK.md`, `.github/copilot-instructions.md`, `docs/integrations/fiap-portal-helper.md`.

### Checklist
- [x] Pasta `fiap-cursor-framework/` com README, CONTRIBUTING, .gitignore
- [x] Rules `fiap-task-intake`, `fiap-task-status`, `fiap-retrospective`, git-workflow, documentation, python-standards, r-standards
- [x] Cópia de `knowledge/` + título neutro em `knowledge/README.md`
- [x] Script `sync_knowledge.sh` com `FIAP_KNOWLEDGE_DEST`
- [x] Verificação: sem ocorrências "wolf" / "WOLF" em `fiap-cursor-framework/`
- [x] `git init`, branch `main`, commits locais
- [x] IDE-agnóstico: `docs/FRAMEWORK.md`, README e `.cursorrules` com ponte, `.github/copilot-instructions.md`, `.cursorrules` sem Task tool / Auto-Premium proprietários
- [x] `docs/integrations/fiap-portal-helper.md` (ética, segredos, portal→knowledge)
- [x] `.gitignore` com padrões `.env` / credenciais locais + `LOCAL.md`
- [x] `SETUP.md`, `GROUP.md`, `LOCAL.example.md` — onboarding grupo + nome no clone
- [x] Templates spec-driven em `docs/templates/`
- [x] Workflows operacionais em `docs/workflows/`
- [x] `setup.py` interativo sem dependências externas
- [x] Exemplo sanitizado `specs/examples/farmtech-notebooks/`
- [x] README/SETUP/workflows com exemplos claros para colar task no chat, anexar PDF de aula ou colar texto copiado da página
- [ ] Criar repo no GitHub (ex.: `fiap-cursor-framework`), `git remote add origin …`, `git push` (quando o Higor pedir)

### Pendências (Higor)
1. Criar repositório vazio no GitHub e `git remote add origin …` + `git push -u origin main`
2. Partilhar URL com Vini, Igor e Salim

---

<!-- TEMPLATE PARA NOVAS TASKS (copiar e preencher):

## Task N — [Nome]
- **Status**: NÃO INICIADA | EM ANDAMENTO | CONCLUÍDA
- **Pasta**: `taskN_nome/`
- **Disciplina**: [qual]

### Checklist de Requisitos
- [ ] (a) ...

### Entregáveis
- [ ] arquivo...

### Pendências (só o Higor pode fazer)
1. ...

-->
