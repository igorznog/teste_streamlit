# Contribuir

## O que é este repo

Template partilhável: [`docs/FRAMEWORK.md`](docs/FRAMEWORK.md) (workflow agnóstico de IDE), regras extra para [Cursor](.cursor/rules/), [instruções Copilot](.github/copilot-instructions.md), `TASK_REGISTRY` em branco e `knowledge/` de exemplo. **Não** inclui entregas concluídas de disciplinas (mantenha-as noutro repositório ou localmente, conforme a política da cadeira).

**Identificação do grupo:** mantém [`GROUP.md`](GROUP.md) preenchido e **commitado** (número do grupo, membros, partes). Cada pessoa usa [`LOCAL.example.md`](LOCAL.example.md) → `LOCAL.md` (no `.gitignore`) para o assistente saber **quem está neste clone**. Guia: [`SETUP.md`](SETUP.md).

**Credenciais** (portal FIAP, APIs): nunca commitar; usar variáveis de ambiente ou ficheiros locais fora do Git (ver [.gitignore](.gitignore)).

## Fluxo de mudanças

1. Crie uma branch a partir de `main`.
2. Faça alterações pequenas e claras (uma regra, um doc, etc.).
3. Abra Pull Request para `main` com descrição em frases completas.

## O que evitar

- Commits com credenciais, tokens ou dados pessoais de terceiros.
- Ficheiros enormes sem necessidade (datasets, ZIPs de entrega) — use `.gitignore` ou anexe noutro sítio conforme o enunciado.

## Manutenção

Quem mantém o repo “oficial” do grupo define se aceita PR de todos ou só de mantenedores.
