# MANUAL DE ENTREGA — Task 1 FarmTech Solutions

**Aluno:** Higor | **Curso:** FIAP  
**Startup:** FarmTech Solutions | **Squad:** WOLF

---

## 1. VISÃO GERAL DO PROJETO

Esse projeto simula uma aplicação para uma fazenda que está migrando para Agricultura Digital. Ele tem **duas partes**:

- **Python** — Aplicação CLI (terminal) com CRUD de culturas + cálculo de área + manejo de insumos
- **R** — Dois scripts: um que analisa estatisticamente os dados da fazenda, e outro (ir além) que consulta dados climáticos de uma API pública

### Estrutura de arquivos

```
task1_farmtech/
├── main.py                 ← Ponto de entrada. Menu interativo no terminal
├── culturas.py             ← Toda a lógica: cálculos, CRUD, exportação CSV
├── estatistica.R           ← Lê os CSVs do Python e calcula média/desvio
├── clima_estatistica.R     ← Consulta API Open-Meteo (ir além)
├── link_video.txt          ← Onde colar o link do YouTube
├── dados_culturas.csv      ← (gerado ao exportar no Python)
├── dados_manejos.csv       ← (gerado ao exportar no Python)
└── MANUAL_ENTREGA.md       ← Este arquivo
```

---

## 2. O QUE CADA ARQUIVO FAZ

### 2.1 `culturas.py` — O cérebro da aplicação

Este módulo contém TODA a lógica de negócio. Nada nele roda sozinho — ele é importado pelo `main.py`.

**O que tem dentro:**

- **Dois vetores** (listas de dicionários): `culturas[]` e `manejos[]` — armazenam todos os dados em memória
- **Cálculo de área:**
  - Cana-de-açúcar → retângulo: `comprimento × largura`
  - Café → círculo: `π × raio²`
- **Cálculo de manejo de insumos:** o usuário informa a dosagem por metro (mL), o número de ruas da lavoura e o comprimento de cada rua. O sistema calcula:
  - `metros_totais = num_ruas × comprimento_rua`
  - `total_produto_ml = dosagem_por_metro × metros_totais`
  - `total_produto_litros = total_ml / 1000`
- **CRUD de culturas:** criar, listar, buscar por ID, atualizar, deletar
- **CRUD de manejos:** criar, listar, buscar por ID, atualizar, deletar
- **Exportação CSV:** gera `dados_culturas.csv` e `dados_manejos.csv` para uso no R

### 2.2 `main.py` — A interface com o usuário

É o arquivo que você roda. Apresenta o menu no terminal e chama as funções do `culturas.py`.

**Menu:**

```
[CULTURAS]
 1. Cadastrar cultura
 2. Listar culturas
 3. Buscar cultura por ID
 4. Atualizar cultura
 5. Deletar cultura

[MANEJO DE INSUMOS]
 6. Cadastrar manejo de insumos
 7. Listar manejos
 8. Atualizar manejo
 9. Deletar manejo

[EXPORTAÇÃO]
 10. Exportar dados para CSV (para uso no R)

 0. Sair
```

**Conceitos que demonstra para a FIAP:**
- Loop `while True` com `break` (item f)
- Decisão `if/elif` em vários pontos (item f)
- `try/except` para tratar erros de entrada (item f)
- Dados em vetores/dicionários (item d)
- Menu com entrada, saída, atualização, deleção e sair (item e)

### 2.3 `estatistica.R` — Estatísticas dos dados da fazenda (obrigatório)

Lê os arquivos CSV exportados pelo Python e calcula:
- Média e desvio padrão das **áreas** (geral e por tipo de cultura)
- Média e desvio padrão dos **manejos** (total de produto em litros, dosagem por metro)

Não precisa de nenhum pacote externo — usa apenas R base.

**Atende o item (g):** "usar esses dados para desenvolver uma aplicação em R para calcular dados estatísticos básicos, como média e desvio."

### 2.4 `clima_estatistica.R` — API climática (ir além)

Consulta a API pública **Open-Meteo** para obter previsão horária de temperatura para São Paulo (região canavieira). Calcula média, desvio padrão, mínima e máxima.

Usa apenas o pacote `jsonlite` (a conexão HTTP é feita com R base).

**Atende o "Ir além":** "usando R, conectar-se a uma API meteorológica pública para coletar dados climáticos."

---

## 3. COMO RODAR TUDO (passo a passo)

### Pré-requisitos

- Python 3.10+ instalado
- R 4.x instalado
- Pacote `jsonlite` no R (já instalado no seu ambiente)

### Passo 1 — Rodar a aplicação Python

```bash
cd ~/fiap_squad_deliverables/task1_farmtech
python main.py
```

### Passo 2 — Dentro do menu Python, fazer o fluxo completo

1. **Opção 1** — Cadastrar uma Cana-de-açúcar (ex: comprimento 200, largura 150)
2. **Opção 1** — Cadastrar um Café (ex: raio 80)
3. **Opção 2** — Listar culturas (mostra tabela com ID, tipo e área)
4. **Opção 3** — Buscar por ID (digitar 1)
5. **Opção 6** — Cadastrar manejo de insumos (ex: Cana, Herbicida, 500 mL/m, 50 ruas, 200m cada)
6. **Opção 6** — Cadastrar outro manejo (ex: Café, Fosfato, 300 mL/m, 30 ruas, 150m cada)
7. **Opção 7** — Listar manejos (mostra tabela com todos os dados e totais calculados)
8. **Opção 4** — Atualizar uma cultura (mudar dimensões)
9. **Opção 8** — Atualizar um manejo (mudar dosagem)
10. **Opção 10** — Exportar dados para CSV
11. **Opção 5** — Deletar uma cultura
12. **Opção 0** — Sair

### Passo 3 — Rodar a estatística em R (dados da fazenda)

```bash
cd ~/fiap_squad_deliverables/task1_farmtech
Rscript estatistica.R
```

Vai mostrar a tabela de culturas e manejos lidos do CSV, seguida de média e desvio padrão.

### Passo 4 — Rodar a consulta climática em R (ir além)

```bash
Rscript clima_estatistica.R
```

Vai mostrar a previsão de temperatura para SP e as estatísticas.

---

## 4. ROTEIRO DO VÍDEO (até 5 minutos)

### Abertura (~20 segundos)
> "Olá, meu nome é Higor, aluno da FIAP. Esse é o projeto da Task 1 da FarmTech Solutions. Vou demonstrar a aplicação Python com CRUD de culturas e manejo de insumos, e os scripts R com estatísticas e consulta a API climática."

### PARTE 1 — Python (~2 min 30s)

**Mostrar o terminal. Rodar `python main.py`.**

> "A aplicação roda pelo terminal. Temos um menu com opções para culturas, manejo de insumos e exportação."

1. **Cadastrar Cana-de-açúcar** (opção 1):
   > "Vou cadastrar uma Cana-de-açúcar. A área é calculada como retângulo: comprimento vezes largura."
   - Digitar: comprimento 200, largura 150
   - Mostrar a confirmação com o ID e a área calculada

2. **Cadastrar Café** (opção 1):
   > "Agora um Café. A área é calculada como círculo: pi vezes raio ao quadrado."
   - Digitar: raio 80

3. **Listar culturas** (opção 2):
   > "Listando todas as culturas cadastradas com seus IDs e áreas."

4. **Cadastrar manejo** (opção 6):
   > "Vou cadastrar o manejo de insumos. Escolho a cultura, o produto, informo a dosagem por metro, o número de ruas e o comprimento de cada rua. O sistema calcula o total necessário."
   - Escolher Cana, Herbicida, 500 mL/m, 50 ruas, 200m

5. **Listar manejos** (opção 7):
   > "Aqui vemos o manejo cadastrado com o total calculado em litros."

6. **Atualizar cultura** (opção 4):
   > "Posso atualizar qualquer registro informando o ID."
   - Atualizar o ID 1 com novas dimensões

7. **Deletar cultura** (opção 5):
   > "E deletar registros pelo ID."
   - Deletar o ID 2

8. **Exportar CSV** (opção 10):
   > "A opção 10 exporta os dados em CSV, que serão consumidos pelo R."

9. **Sair** (opção 0)

### PARTE 2 — R Estatístico (~1 min)

**Rodar `Rscript estatistica.R`**

> "Agora no R, o script lê os CSVs que o Python exportou e calcula média e desvio padrão das áreas e dos manejos."

- Mostrar a saída com os dados e as estatísticas

### PARTE 3 — R API Climática (~1 min)

**Rodar `Rscript clima_estatistica.R`**

> "Como 'ir além', este script consulta a API Open-Meteo para obter dados de temperatura de São Paulo e calcula as estatísticas."

- Mostrar a saída com temperaturas e média/desvio

### Encerramento (~20 segundos)
> "O código está versionado no GitHub. Essa foi a demonstração completa da Task 1. Obrigado!"

---

## 5. VALORES SUGERIDOS PARA USAR NA DEMONSTRAÇÃO

Para facilitar e não ter que inventar números na hora do vídeo:

| Ação | Valores |
|---|---|
| Cadastrar Cana-de-açúcar | Comprimento: 200, Largura: 150 |
| Cadastrar Café | Raio: 80 |
| Cadastrar 2ª Cana | Comprimento: 300, Largura: 100 |
| Manejo Cana (Herbicida) | Dosagem: 500 mL/m, 50 ruas, 200m cada |
| Manejo Café (Fosfato) | Dosagem: 300 mL/m, 30 ruas, 150m cada |
| Atualizar cultura ID 1 | Mudar para Cana 250 × 120 |
| Atualizar manejo ID 1 | Nova dosagem: 600 mL/m, 55 ruas, 210m |

---

## 6. CHECKLIST ANTES DE ENTREGAR

- [ ] Python rodou sem erros (todas as opções do menu testadas)
- [ ] CSVs foram gerados (opção 10)
- [ ] `Rscript estatistica.R` rodou e mostrou média/desvio
- [ ] `Rscript clima_estatistica.R` rodou e mostrou dados da API
- [ ] Vídeo gravado (até 5 min), postado no YouTube como "não listado"
- [ ] Link do vídeo colado no `link_video.txt`
- [ ] Resumo do artigo da Embrapa (item h) — 1 folha A4, Arial 11, espaço 1
- [ ] Tudo commitado no GitHub
- [ ] ZIP gerado com: Python, R, resumo do artigo, link_video.txt

---

## 7. COMO GERAR O ZIP FINAL

Após completar tudo (incluindo o resumo do artigo e o link do vídeo):

```bash
cd ~/fiap_squad_deliverables
zip -r task1_farmtech_WOLF.zip task1_farmtech/ -x "task1_farmtech/__pycache__/*"
```

O ZIP vai conter todos os arquivos `.py`, `.R`, `link_video.txt`, o resumo e este manual.

---

## 8. ITENS PENDENTES (SÓ VOCÊ PODE FAZER)

1. **Resumo do artigo** (item h) — O artigo é esse: https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1003485/1/CAP8.pdf
   - 1 folha A4, fonte Arial 11, espaçamento 1, margens 2cm
   - Salvar como PDF ou DOCX dentro de `task1_farmtech/`

2. **Gravar o vídeo** — Use o roteiro da seção 4 acima. Pode usar gravador de tela (OBS, StreamYard) ou celular filmando a tela.

3. **Postar no YouTube** como "não listado" e colar o link no `link_video.txt`.

4. **Criar repositório no GitHub** e fazer push (posso te ajudar com isso).
