# agent-browser × Portal FIAP On

[`vercel-labs/agent-browser`](https://github.com/vercel-labs/agent-browser)
é uma CLI nativa em Rust feita para agentes de IA controlarem um navegador
real. Funciona em Cursor, Claude Code, Codex, Gemini CLI, Copilot, Goose,
OpenCode, Windsurf — e como é apenas um binário no `PATH`, qualquer IDE com
shell consegue invocá-la.

Para o nosso fluxo de captura do FIAP On, ela substitui com vantagem o
script Playwright caseiro: zero código próprio, instalação cross-platform,
sessão persistente e auth vault embutido.

## 1. Instalação (uma vez por máquina)

Escolha um dos canais:

```bash
# npm (mais comum)
npm install -g agent-browser
agent-browser install            # baixa Chromium oficial

# macOS (Homebrew)
brew install agent-browser
agent-browser install

# Rust (Cargo)
cargo install agent-browser
agent-browser install
```

No Linux/WSL2, se faltar lib de sistema:

```bash
agent-browser install --with-deps
```

Diagnóstico:

```bash
agent-browser doctor
```

## 2. Instalar a skill oficial no seu IDE (uma vez)

```bash
npx skills add vercel-labs/agent-browser
```

Funciona com Cursor, Claude Code, Codex, Cursor Code, Gemini CLI,
GitHub Copilot, Goose, OpenCode e Windsurf. A skill é apenas um stub que
aponta para `agent-browser skills get core`, então fica sempre alinhada com
a versão do binário.

## 3. Autenticação no Portal FIAP On (uma vez por sessão longa)

Três caminhos, escolha o que se encaixa:

### 3.1 Auth vault (recomendado)

Credenciais ficam criptografadas em `~/.agent-browser/`. O LLM nunca vê a
senha.

```bash
# Gere uma chave de criptografia uma vez (ou deixe o vault gerar)
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)

# Grave o login da FIAP (a senha vem pelo stdin, fora do prompt do agente)
echo "SUA_SENHA_AQUI" | agent-browser auth save fiap-on \
    --url https://on.fiap.com.br/login/index.php \
    --username SEU_USUARIO \
    --password-stdin

# Use a partir de agora
agent-browser auth login fiap-on
```

> A senha é digitada **uma vez** no terminal, vai direto para o vault
> criptografado e nunca aparece em logs nem é enviada para o modelo.

### 3.2 Reuso do perfil do Brave (login já feito)

Se você já está logado no Brave:

```bash
# Linux/WSL2
agent-browser \
  --executable-path /usr/bin/brave-browser \
  --profile "$HOME/.config/BraveSoftware/Brave-Browser" \
  open https://on.fiap.com.br/local/conteudocurso/
```

```bash
# macOS
agent-browser \
  --executable-path "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
  --profile "$HOME/Library/Application Support/BraveSoftware/Brave-Browser" \
  open https://on.fiap.com.br/local/conteudocurso/
```

> `--profile` copia o perfil para um diretório temporário (snapshot
> read-only), então não corrompe o seu Brave normal.

### 3.3 Auto-connect a um Brave já aberto com remote-debugging

```bash
# Abra o Brave assim:
brave-browser --remote-debugging-port=9222

agent-browser --auto-connect open https://on.fiap.com.br/local/conteudocurso/
agent-browser --auto-connect state save ~/.agent-browser/fiap-state.json

# Depois reuse:
agent-browser --state ~/.agent-browser/fiap-state.json open https://on.fiap.com.br/...
```

## 4. Captura do curso inteiro (recomendado)

O orquestrador `scripts/fiap_capture_all_phases.py` faz login, percorre cada
FASE, identifica capítulos e baixa o **e-book PDF** de cada um (forma mais
rápida e canônica de pegar o conteúdo completo).

```bash
# Tudo: todas as fases liberadas, só PDFs (~30 MB para a grade atual)
python3 scripts/fiap_capture_all_phases.py

# Smoke test: 2 capítulos da Fase 3
python3 scripts/fiap_capture_all_phases.py --phases 3 --max-chapters 2

# PDFs + ZIPs de assets
python3 scripts/fiap_capture_all_phases.py --assets

# Também salvar conteúdo HTML iterando slides (LENTO; só se pedido)
python3 scripts/fiap_capture_all_phases.py --slides
```

Saída em `docs/validation/captures/fases/<faseN>/cap<NN>_<slug>/<arquivo>.pdf`
com `INDEX.json` agregado. Veja `docs/validation/fiap_pdfs_captured.md` para
detalhes de como o download funciona (cookies, Referer, dedupe de fases).

## 4.1 Captura ad-hoc de uma página

Quando precisar de uma URL específica fora do fluxo do curso:

```bash
# Sessão isolada para o FIAP, com state persistente
agent-browser --session-name fiap-on auth login fiap-on
agent-browser --session-name fiap-on open "https://on.fiap.com.br/<URL>"
agent-browser --session-name fiap-on wait --load networkidle
agent-browser --session-name fiap-on snapshot -i --urls --json \
    > docs/validation/captures/pagina.json
agent-browser --session-name fiap-on screenshot --annotate --full \
    docs/validation/captures/pagina.png
agent-browser --session-name fiap-on eval "document.documentElement.outerHTML" \
    > docs/validation/captures/pagina.html
```

## 5. Modo agente em linguagem natural (opcional)

Se você configurar `AI_GATEWAY_API_KEY` (Vercel AI Gateway), dá pra falar
em PT-BR direto:

```bash
agent-browser chat \
  "abra a Fase 3 no portal FIAP, capture o capítulo 1 com screenshot anotado \
   e salve o texto em docs/validation/captures/fase3-cap1.txt"
```

## 6. Segurança no contexto FIAP

- Vault criptografado: senha nunca vai pro chat.
- `--allowed-domains "on.fiap.com.br,*.fiap.com.br"` bloqueia navegação
  fora do portal (defesa contra prompt injection).
- `--confirm-actions eval,download` exige confirmação para ações sensíveis.
- `--max-output 50000` evita estourar contexto do LLM com páginas enormes.
- Submissões avaliativas (Fast Test/quiz) continuam manuais. Use só para
  ler e organizar.

## 7. Como o nosso parser conversa com o agent-browser

Saídas do `agent-browser` (txt/json/png/html) vão para
`docs/validation/captures/`. Depois:

```bash
# Cole o .txt no template (ou use o snapshot --json direto)
python3 scripts/parse_fiap_task_capture.py docs/templates/FIAP_TASK_CAPTURE_TEMPLATE.md
```

Gera `docs/validation/fiap_capture_parsed.{md,json}` estruturado.

## 8. Quando preferir Playwright caseiro vs agent-browser

| Cenário                                            | Use                |
|----------------------------------------------------|--------------------|
| Máquina com npm/cargo/brew e qualquer IDE          | **agent-browser**  |
| Máquina restrita só com Python                     | `scripts/fiap_portal_capture.py` (Playwright) |
| Ambiente offline / portal bloqueando automação     | Template Ctrl+C/V  |

Os três caminhos terminam no mesmo parser e na mesma estrutura
`docs/validation/`.
