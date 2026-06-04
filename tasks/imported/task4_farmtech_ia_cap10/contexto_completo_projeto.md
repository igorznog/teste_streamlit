# Contexto Completo do Projeto — FIAP Fase 3
## Grupo 45 | 1TIAOA | 2026/1

> Texto literal extraído do portal FIAP On em 08/05/2026.
> Prazo de entrega: **Terça-feira, 19 de Maio de 2026, às 23h59**

---

# ATIVIDADE 1 — Cap 1: Etapas de uma Máquina Agrícola

**Tipo:** Atividade em Grupo
**Período:** 22/04/2026 a 19/05/2026

---

## PROJETO FASE 3 – ETAPAS DE UMA MÁQUINA AGRÍCOLA

### Introdução

O PBL (Project-Based Learning) do curso de Inteligência Artificial é uma jornada que simula o crescimento de uma startup.

No nosso caso, essa startup é a FarmTech Solutions, que atua (de forma fictícia) como uma consultoria em soluções para o setor do agronegócio — uma das áreas mais promissoras para aplicação de IA no Brasil, segundo o Global AI Jobs Barometer da PwC (2025).

Mapa mental da estrutura do PBL: https://xmind.ai/share/LwsoOKB2?xid=oErUWyET

---

### Entregas do PBL

O PBL sempre conta com:

- **1 entrega obrigatória** → vale pontos no boletim.
- **2 entregas opcionais (Ir Além)** → não são obrigatórias, mas incentivamos que você e seu grupo explorem.

---

### Entrega Obrigatória — Banco de Dados Oracle

Nesta atividade, vamos explorar conceitos iniciais de Banco de Dados, carregando os dados coletados pelos sensores da Fase 2 em um banco relacional Oracle.

**Você deverá entregar:**

- Um relatório com os passos seguidos;
- Prints de tela das consultas realizadas;
- Uso do arquivo da Fase 2 como base para importação.

#### Passo a Passo no Oracle SQL Developer

1. Faça download do Oracle SQL Developer: https://www.oracle.com/database/sqldeveloper/technologies/download/

2. Faça download da versão correspondente ao seu sistema operacional (Windows, Linux ou Mac OSX). O site pode pedir cadastro gratuito antes do download.

3. Descompacte o arquivo e execute o programa SQLDEVELOPER. **Observação:** é necessário extrair os arquivos e não apenas abrir o arquivo compactado.

4. Clique em "Nova Conexão" (o ícone + em verde).

5. Estabeleça uma conexão com o banco de dados Oracle:
   - **Nome:** informe um nome qualquer, por exemplo, FIAP
   - **Nome do Usuário:** informe o seu RM com as letras RM, por exemplo: RM12345
   - **Senha:** informe sua data de nascimento com seis dígitos no formato DDMMYY (ex: se nasceu em 07/09/2005, a senha é 070905)
   - **Nome do Host:** oracle.fiap.com.br
   - **Porta:** 1521
   - **SID:** ORCL
   - Clique em **Testar**. Se a conta estiver bloqueada, entre em contato com o suporte. Se usuário/senha estiverem inválidos, verifique o formato RM12345.

6. Uma vez conectado, localize o ícone "Tabelas (Filtrado)".

7. Clique com o botão direito em "Tabelas (Filtrado)" e selecione "Importa Dados".

8. Clique em "Procurar" e carregue os dados dos seus sensores.

9. Clique em "Próximo". No campo "Nome da Tabela", defina um nome sem espaços, sem caracteres especiais, começando por letra e com no máximo 30 caracteres.

10. Clique em "Próximo". Selecione os campos que deseja importar (não altere nada para importar todos).

11. Clique em "Próximo". Altere o nome das colunas se necessário.

12. Clique em "Próximo".

13. Clique em "Finalizar" e aguarde a confirmação de importação bem-sucedida.

14. Clique em OK e consulte os dados com: `SELECT * FROM NOME_DA_SUA_TABELA;` (Ctrl+Enter executa o comando).

15. Agora você consegue explorar seus dados fazendo consultas, e eles estão armazenados no banco da Oracle.

---

### Entregáveis — Cap 1 (Obrigatório)

O grupo (1 a 5 alunos) deve entregar:

- Repositório no GitHub organizado (meugit/cursotiao/pbl/fase3/...);
- Arquivo `README.md` documentando o projeto, com prints do banco;
- Códigos C/C++ ou Python usados;
- Vídeo (de até 5 minutos no YouTube como "não listado") mostrando o funcionamento.

---

### Programa Ir Além — Opção 1: Dashboard em Python (opcional)

Crie uma dashboard (Streamlit, Dash etc.) para visualizar:

- Níveis de umidade, P, K e pH;
- Status da irrigação;
- Sugestões de irrigação baseadas em clima.

---

### Programa Ir Além — Opção 2: Machine Learning no Agronegócio (opcional)

Use a base `produtos_agricolas.csv` (variáveis: N, P, K, temperatura, umidade, pH, chuva, label).

**Atividades:**

- Análise exploratória com pelo menos 5 gráficos.
- Identificação do "perfil ideal" de solo/clima para 3 culturas escolhidas.
- Desenvolvimento de 5 modelos preditivos com diferentes algoritmos.
- Avaliação comparativa dos modelos.

**Entregas:**

- Jupyter Notebook (`SeuNome_RMxxxx_fase3_cap1.ipynb`) com código e análises.
- Vídeo (de até 5 minutos no YouTube como "não listado") apresentando o trabalho.

---

### Baremas — Cap 1

#### Entrega Obrigatória (máximo 10 pontos) — Banco de Dados

| Critério | Descrição | Pontos |
|---|---|---|
| Organização do repositório GitHub | Estrutura de pastas clara, README.md presente, arquivos nomeados corretamente. | 2,0 |
| Documentação (README.md) | Explicação detalhada do processo, prints de tela das etapas no Oracle SQL Developer e consulta SELECT *. | 2,0 |
| Carga de dados no Oracle | Importação correta dos dados coletados na Fase 2, evidenciada por prints de tela. | 2,0 |
| Consultas SQL | Execução e apresentação de consultas SQL corretas e funcionais. | 2,0 |
| Vídeo demonstrativo (até 5 min) | Clareza na explicação, mostra o funcionamento do banco e organização do repositório. | 2,0 |
| **Total** | | **10,0** |

#### Ir Além — Dashboard em Python (máximo 5 pontos extras)

| Critério | Descrição | Pontos |
|---|---|---|
| Funcionamento da Dashboard | Visualização clara de pelo menos 3 variáveis (umidade, pH, P/K). | 1,5 |
| Interatividade/Visualização | Gráficos ou tabelas bem apresentados, uso de bibliotecas adequadas. | 1,0 |
| Integração com dados da Fase 2 | Uso correto dos dados coletados no projeto. | 1,0 |
| Documentação no GitHub | README.md explicando a dashboard, prints da interface. | 0,5 |
| Vídeo demonstrativo (até 5 min) | Demonstração clara da dashboard em funcionamento. | 1,0 |
| **Total** | | **5,0** |

#### Ir Além — Machine Learning no Agronegócio (máximo 5 pontos extras)

| Critério | Descrição | Pontos |
|---|---|---|
| Análise exploratória | Pelo menos 5 gráficos com análise descritiva. | 1,0 |
| Discussão sobre o perfil ideal de solo/clima | Identificação clara e comparação com 3 culturas. | 1,0 |
| Modelagem preditiva | Desenvolvimento de 5 modelos com algoritmos distintos. | 1,5 |
| Avaliação de performance | Uso de métricas adequadas, comparação dos modelos. | 1,0 |
| Documentação e Notebook | Notebook bem organizado, README.md e vídeo de apresentação. | 0,5 |
| **Total** | | **5,0** |

---

---

# ATIVIDADE 2 — Cap 10: A Primeira Técnica de Aprendizado de Máquina

**Tipo:** Atividade em Grupo
**Período:** 22/04/2026 a 19/05/2026

---

## ATIVIDADE — Modelagem de IA da FarmTech Solutions

Para essa atividade, você deverá analisar uma base de dados com informações de condições de solo e temperatura, relacionadas com o tipo de produto agrícola. Além da análise da base, você deverá construir alguns modelos preditivos e compará-los em termos da sua performance.

### Base de dados

A base está disponível no arquivo `produtos_agricolas.csv`. As variáveis são:

- **N:** quantidade de nitrogênio no solo;
- **P:** quantidade de fósforo no solo;
- **K:** quantidade de potássio no solo;
- **temperature:** temperatura média da região em graus Celsius;
- **humidity:** umidade média do ar na região;
- **pH:** pH do solo;
- **rainfall:** precipitação em milímetros;
- **label:** tipo de cultura plantada nas condições daquela linha.

### Proposta de atividade

Baseado no dataset apresentado, sua atividade consiste em:

1. Fazer uma **análise exploratória** na base para se familiarizar com os dados;
2. Fazer uma **análise descritiva** narrando os principais achados da base contendo **no mínimo cinco gráficos**;
3. Encontrar o **"perfil ideal" de solo/clima** para as plantações, além de discorrer sobre como os três produtos distintos (à escolha do grupo) se comparam com esse perfil ideal. Por exemplo, preferem maior umidade e mais precipitação? Preferem mais calor e menos fósforo? Para esta parte se apoie em análises estatísticas e/ou visuais;
4. Desenvolver **5 modelos preditivos** (cada um com um algoritmo diferente) que, dadas as condições climáticas e de solo, prevejam qual é o melhor produto agrícola a ser cultivado naquelas características. Esta parte da tarefa inclui seguir as boas práticas dos projetos de Machine Learning, bem como avaliar o modelo com métricas pertinentes ao problema.

### O que será entregue?

Entregue a atividade como um **jupyter notebook** contendo:

- Células de códigos executadas;
- Células de markdown organizando seu relatório e discorrendo textualmente sobre os achados a partir dos dados, e conclusões a respeito dos pontos fortes e limitações do trabalho;
- O nome do arquivo deve conter seu nome completo, RM, fase e capítulo, exemplo: `JoaoSantos_RM76332_fase3_cap2.ipynb`
