# Passo-a-passo — Importar `leituras_sensores.csv` no Oracle SQL Developer

> Wizard nativo "Importar Dados" do Oracle SQL Developer. Não precisa criar a
> tabela antes — o wizard pode criar.

## Pré-requisitos

- Oracle SQL Developer instalado e funcionando (`docs/INSTALAR_ORACLE_SQL_DEVELOPER.md`).
- Conexão ativa configurada com:
  - **Nome**: `FIAP`
  - **Usuário**: `RM571820`
  - **Senha**: sua data de nascimento DDMMYY (6 dígitos)
  - **Host**: `oracle.fiap.com.br`
  - **Porta**: `1521`
  - **SID**: `ORCL`
- Arquivo `dados/leituras_sensores.csv` (1000 linhas) já gerado.

## Wizard de importação (corresponde aos passos 6–13 do enunciado)

### 1. Abrir o nó "Tabelas (Filtrado)"

- Painel **Conexões** → expandir `FIAP` → expandir `Tabelas (Filtrado)`.
- 📸 **prints/01_arvore_conexao.png**

### 2. Iniciar importação

- Botão direito em **Tabelas (Filtrado)** → **Importar Dados…**.
- 📸 **prints/02_importar_data_menu.png**

### 3. Selecionar o arquivo CSV

- Clicar em **Procurar…** → escolher `dados/leituras_sensores.csv`.
- Codificação: **UTF-8**.
- Marcar **Header** (a primeira linha é cabeçalho).
- Delimitador: **vírgula (,)**.
- Linha de visualização aparece com `timestamp,n,p,k,ph,umidade,bomba`.
- 📸 **prints/03_selecionar_arquivo.png** (mostrando a prévia)

### 4. Definir nome da tabela

- Campo **Nome da Tabela**: `LEITURAS_SENSORES`
- Método: **Inserção** (Insert).
- 📸 **prints/04_nome_tabela.png**

### 5. Selecionar colunas

- Mantenha as 7 colunas marcadas: `timestamp, n, p, k, ph, umidade, bomba`.
- 📸 **prints/05_colunas.png**

### 6. Ajustar tipos das colunas

Renomear (caso queira preservar o padrão Oracle) e definir tipos:

| Origem CSV  | Coluna Oracle | Tipo         | Precisão/Escala |
|-------------|--------------|--------------|-----------------|
| timestamp   | TS           | TIMESTAMP    | (default)       |
| n           | N            | NUMBER       | 1               |
| p           | P            | NUMBER       | 1               |
| k           | K            | NUMBER       | 1               |
| ph          | PH           | NUMBER       | 4,2             |
| umidade     | UMIDADE      | NUMBER       | 5,2             |
| bomba       | BOMBA        | NUMBER       | 1               |

> Se o wizard reclamar do formato do timestamp, use:
> `YYYY-MM-DD HH24:MI:SS`

- 📸 **prints/06_tipos_colunas.png**

### 7. Pré-visualização

- Conferir as 5 primeiras linhas com tipos corretos.
- 📸 **prints/07_preview.png**

### 8. Finalizar

- Clicar em **Concluir**.
- Aguardar a mensagem **"1000 linhas importadas com sucesso"** (ou similar).
- 📸 **prints/08_concluido.png** (mensagem de sucesso)

### 9. Conferir importação

No SQL Worksheet (Alt+F10), rodar:

```sql
SELECT COUNT(*) FROM leituras_sensores;
-- esperado: 1000

SELECT * FROM leituras_sensores FETCH FIRST 10 ROWS ONLY;
```

- 📸 **prints/09_count_query.png**
- 📸 **prints/10_select_all.png**

### 10. (Opcional) Adicionar PK e índices

Se a tabela criada pelo wizard não tem PK, rode `sql/01_criar_tabela.sql`
**antes** do import — ou execute apenas os blocos `CREATE INDEX` depois:

```sql
ALTER TABLE leituras_sensores ADD CONSTRAINT pk_leituras PRIMARY KEY (ts);
CREATE INDEX ix_leituras_ts    ON leituras_sensores(ts);
CREATE INDEX ix_leituras_bomba ON leituras_sensores(bomba);
```

## Próximos prints (rodando `03_consultas.sql`)

- 📸 **prints/sql_q3_estatisticas.png** (Q3 — médias e desvios)
- 📸 **prints/sql_q4_bomba.png** (Q4 — percentual bomba ligada)
- 📸 **prints/sql_q6_perfil_diario.png** (Q6 — pH/umidade por hora)
- 📸 **prints/sql_q8_alertas.png** (Q8 — solo seco com bomba desligada)

## Checklist final desta etapa

- [ ] Tabela `LEITURAS_SENSORES` existe com 1000 linhas.
- [ ] Tira 10+ prints conforme lista acima e salva em `prints/`.
- [ ] Conferiu que o `SELECT *` retorna os dados.
- [ ] Rodou as 10 queries do `03_consultas.sql` sem erro.
