# Dashboards estáticos do workflow

Esta pasta tem visões simples em HTML para abrir direto no navegador e compartilhar com o grupo.

## Arquivos

- [`index.html`](index.html) — entrada visual central para o aluno encontrar status, onboarding e próximos passos.
- [`grupo.html`](grupo.html) — visão geral do grupo: tarefas da disciplina, pendências, membros e links rápidos.
- [`individual.html`](individual.html) — visão por integrante, com seletor de membro, foco atual, checklist e prompts úteis.
- [`registry.html`](registry.html) — versão visual do `TASK_REGISTRY.md`: entregas da disciplina em destaque; tasks de desenvolvimento do workflow ficam em seção separada.

## O que entra em cada painel

- **Disciplina (FIAP):** entregas, prazos, specs e pendências das tasks acadêmicas.
- **Workflow (infra):** por exemplo validação do repositório (Task 5) — aparece só no registry, não nas métricas do grupo.
- **Grupo:** enquanto o número não estiver em `GROUP.md`, os painéis mostram *FIAP Group (número a definir)*.

## Como abrir

Abra o arquivo no navegador pelo explorador de arquivos ou pelo GitHub:

```text
docs/dashboard/index.html
docs/dashboard/grupo.html
docs/dashboard/individual.html
docs/dashboard/registry.html
```

## Como manter atualizado

Os dados são gerados a partir de `TASK_REGISTRY.md` e `GROUP.md`.

Depois de atualizar status, prazos, membros ou pendências, rode:

```bash
python scripts/update_workflow_dashboard.py
```

Isso recria os HTMLs da pasta sem ler `LOCAL.md`.

## Integração com agentes

- Cursor: `.cursor/hooks.json` roda `.cursor/hooks/sync-dashboard.sh` após edições. O hook é silencioso e fail-open.
- Outros agentes/IDEs: após alterar `TASK_REGISTRY.md` ou `GROUP.md`, rode `python scripts/update_workflow_dashboard.py --quiet`.
- CI ou revisão: use `python scripts/update_workflow_dashboard.py --check` para falhar se os HTMLs estiverem desatualizados.

## Regras

- Não depende de `LOCAL.md`.
- Não mostra senhas, cookies ou dados sensíveis.
- Não é tempo real no navegador: é um snapshot versionável.
- Não substitui `TASK_REGISTRY.md`; é uma visão rápida para o grupo.
