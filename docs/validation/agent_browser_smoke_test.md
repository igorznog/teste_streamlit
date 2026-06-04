# Smoke Test — agent-browser × Portal FIAP

Validação local executada em 17/05/2026 (WSL2 Ubuntu, Node 20.18.2).

## Versão instalada

```
agent-browser 0.27.0
Chrome for Testing 148.0.7778.167 em /home/higor/.agent-browser/browsers/
Skill oficial em .agents/skills/agent-browser/SKILL.md
```

`agent-browser doctor --offline --quick` → 6 pass, 0 warn, 0 fail.

## Roteiro executado

```bash
npm install -g agent-browser
agent-browser install
npx -y skills add vercel-labs/agent-browser

agent-browser open https://on.fiap.com.br
agent-browser wait --load networkidle
agent-browser get title       # FIAP EAD - Login
agent-browser get url         # https://on.fiap.com.br/
agent-browser screenshot --full docs/validation/captures/fiap_homepage_test.png
agent-browser snapshot -i --urls
agent-browser close
```

## Snapshot real da página de login

```
- heading "CONECTE-SE COM SUA JORNADA ACADÊMICA" [level=1, ref=e2]
- textbox "USUÁRIO*" [required, ref=e3]
- textbox "SENHA*"   [required, ref=e4]
- button  "Mostrar/ocultar senha"  [ref=e5]
- button  "LOGAR"    [disabled, ref=e6]
- button  "Esqueci minha senha."   [ref=e7]
- link    "11 98170-0028" [ref=e1, url=https://wa.me/5511981700028]
```

## Implicações práticas

- A pipeline de login pode ser scriptada usando os refs acima:

  ```bash
  agent-browser open https://on.fiap.com.br
  agent-browser snapshot -i
  agent-browser fill @e3 "<usuario>"      # campo USUÁRIO
  agent-browser fill @e4 "<senha-do-vault>"  # campo SENHA
  agent-browser click @e6                 # botão LOGAR
  agent-browser wait --load networkidle
  ```

- O fluxo recomendado segue sendo o **auth vault** (`agent-browser auth save fiap-on …`)
  para a senha não trafegar como argumento.

- Screenshot e PNGs ficam em `docs/validation/captures/` (já no `.gitignore`).

## Próximos passos manuais

1. Higor define `AGENT_BROWSER_ENCRYPTION_KEY` no shell. ✅ feito (17/05/2026)
2. Higor grava a credencial uma vez via `agent-browser auth save fiap-on`. ✅ feito
3. Higor confirma se quer abrir issue no repo do grupo orientando os colegas
   a instalar `agent-browser` + `npx skills add vercel-labs/agent-browser`.

## Validação end-to-end com auth (17/05/2026 17:30)

Após o aluno gravar a credencial no vault, executei batch único:

```bash
agent-browser batch --bail \
  "auth login fiap-on" \
  "wait --load networkidle" \
  "screenshot --full docs/validation/captures/fiap_dashboard.png" \
  "open https://on.fiap.com.br/local/conteudocurso/" \
  "wait --load networkidle" \
  "screenshot --full docs/validation/captures/fiap_fase3_home.png" \
  "snapshot -i --urls" \
  "close"
```

Resultados reais capturados:

- Dashboard pessoal: `Home` em `https://on.fiap.com.br/local/home/`
  ("Boa tarde, Higor.").
- Página Aulas-Fases: `https://on.fiap.com.br/local/conteudocurso/`
  com Fase 3 ("Colheita De Dados E Insights", 22/04/2026 → 19/05/2026).
- Detectou todos os 11 capítulos + How To Google Colab, cada um com:
  - Link "Acessar conteúdo" (mod/conteudoshtml/view.php?id=...)
  - Link "Acessar E-Book" (mod/conteudospdf/view.php?id=...)
  - ZIP de assets quando aplicável (Cap 9, 10, How To)
- Detectou 5 entregas (4 assignments + 1 quiz) com IDs reais:
  605373, 605374, 605361 (quiz), 605883, 614387.
- Detectou links externos: Google Drive de assets, GitHub template.

## Conclusão

A pipeline completa funciona ponta a ponta:

`agent-browser auth login` → carrega session-cookies →
`open URL` autenticado → `snapshot --urls` → `screenshot --full` → `close`

Pronto para o grupo replicar via `bash scripts/setup_fiap_automation.sh`.
