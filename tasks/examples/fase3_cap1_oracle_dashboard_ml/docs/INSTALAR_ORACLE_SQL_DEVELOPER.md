# Instalar Oracle SQL Developer (Windows + WSL2)

> Recomendado: instalar **no Windows nativo** (não dentro do WSL2). É mais
> rápido, abre os prints em janelas Windows naturais e funciona sem GUI no
> Linux. Como você está num Windows com WSL2, é o caminho mais simples.

## Caminho A — Windows nativo (recomendado)

### 1. Pré-requisito: Java JDK 17 ou 21

Oracle SQL Developer **24.x** já vem com Java embutido. Baixe a versão
**"with JDK"** que não precisa instalar Java separado.

### 2. Download

Acesse: <https://www.oracle.com/database/sqldeveloper/technologies/download/>

- Aceite os termos.
- Faça login (gratuito) ou crie uma conta Oracle se nunca usou.
- Baixe **"Windows 64-bit with JDK 17 included"** (~470 MB).
  - Nome do arquivo típico: `sqldeveloper-24.3.1.347.1826-x64.zip`.

### 3. Instalação

1. Descompacte o ZIP em `C:\oracle\sqldeveloper\` (ou onde preferir).
2. Não tem instalador — é só descompactar.
3. Executar **`sqldeveloper.exe`** dentro da pasta descompactada.
4. Na primeira execução, ele pede para criar atalho — aceite.
5. Pode demorar 30–60 s para abrir a primeira vez.

### 4. Configurar conexão FIAP

1. Painel **Conexões** (esquerda) → botão **+** verde (Nova Conexão).
2. Preencher:
   - **Nome**: `FIAP`
   - **Usuário**: `RM000000` (seu RM com letras maiúsculas)
   - **Senha**: sua data de nascimento DDMMYY (6 dígitos)
   - **Salvar Senha**: marcar (opcional)
   - **Tipo de Conexão**: `Básico`
   - **Nome do Host**: `oracle.fiap.com.br`
   - **Porta**: `1521`
   - **SID**: `ORCL` (NÃO usar Service Name)
3. Clicar em **Testar**.
   - ✅ Sucesso → clicar **Conectar**.
   - ❌ "Usuário/senha inválido" → conferir se o RM está em maiúsculas. Se
     continuar falhando, abrir chamado no helpcenter FIAP pedindo reset.
   - ❌ "Conta bloqueada" → abrir chamado pedindo desbloqueio.
   - ❌ "Listener não conhece o serviço" → verificar que escolheu **SID** e
     não Service Name.

### 5. Validar acesso

No Worksheet (Alt+F10):

```sql
SELECT USER, SYSDATE FROM dual;
```

Se retornar `RM000000` + data/hora atual, está pronto.

## Caminho B — WSL2 (mais avançado)

Funciona, mas precisa de X-Server no Windows (VcXsrv, X410 ou Windows 11
WSLg nativo) e instalar Java separado. Use só se o Caminho A der problema.

```bash
# Pré-requisitos
sudo apt update
sudo apt install -y openjdk-17-jdk unzip

# Download manual via navegador (Oracle exige login)
# Baixe a versão "Other Platforms" e mova para ~/Downloads
cd ~
unzip ~/Downloads/sqldeveloper-24.3.1.347.1826-no-jre.zip
cd sqldeveloper
./sqldeveloper.sh
```

No primeiro `./sqldeveloper.sh` ele perguntará o caminho do Java:
`/usr/lib/jvm/java-17-openjdk-amd64`.

## Caminho C — Alternativa: SQL Developer Web (sem instalar)

A FIAP pode disponibilizar acesso via navegador em algumas turmas. Verifique
em <https://on.fiap.com.br> menu **Serviços** → **Oracle SQL Developer Web**.

**NÃO recomendado para esta entrega** porque o enunciado pede prints do
**SQL Developer desktop** e algumas telas são exclusivas do app.

## Problemas comuns

| Sintoma | Solução |
|--------|---------|
| `java.lang.OutOfMemoryError` | Editar `sqldeveloper.conf` → `AddVMOption -Xmx2048M`. |
| Listener: ORA-12514 | Você marcou "Service Name". Trocar para **SID** e usar `ORCL`. |
| Senha bloqueada após 3 tentativas | Abrir chamado helpcenter pedindo desbloqueio (não dá pra resetar sozinho). |
| Acentos aparecem como `??` | Em **Ferramentas > Preferências > Ambiente > Codificação**, definir **UTF-8**. |
| Wizard Importar Dados não aceita timestamp | Forçar formato: `YYYY-MM-DD HH24:MI:SS` na etapa de tipos. |

## Checklist de "pronto pra começar"

- [ ] Conexão `FIAP` salva no painel Conexões.
- [ ] `SELECT USER FROM dual;` retorna seu RM.
- [ ] Você consegue ver o nó **Tabelas (Filtrado)** ao expandir a conexão.
- [ ] Tira print da árvore com a conexão verde → `prints/00_conexao_ok.png`.
