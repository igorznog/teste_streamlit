# Workflow 00 — Onboarding de colega

Use quando um novo membro do grupo clonar o repositorio ou quando alguem trocar de IDE/maquina.

## Objetivo

Fazer o aluno chegar rapidamente a tres estados:

- identidade local configurada em `LOCAL.md`;
- contexto do grupo alinhado em `GROUP.md`;
- primeiro pedido correto para a IA, sem depender de memoria informal.

## Pre-requisitos

- Git instalado.
- Python 3.10+.
- Acesso ao repositorio do grupo.
- Node.js 20+ somente se quiser automacao do portal FIAP.

## Jornada curta

1. Clonar o repositorio e abrir no IDE.
2. Rodar `python setup.py`.
3. Revisar `LOCAL.md` e `GROUP.md`.
4. Abrir `docs/dashboard/index.html` para entender status, fase atual e próximos passos.
5. Ler `README.md`, `SETUP.md` e `docs/FRAMEWORK.md`.
6. Se quiser capturar portal automaticamente, rodar `bash scripts/setup_fiap_automation.sh`.
7. Fazer uma conversa teste com a IA usando um dos prompts abaixo.

## Painel visual

Os HTMLs em `docs/dashboard/` ajudam o aluno a se localizar rapidamente:

- `index.html` — entrada central.
- `grupo.html` — visão do grupo.
- `individual.html` — visão por integrante.
- `registry.html` — `TASK_REGISTRY.md` visual com filtros.

Eles não são tempo real. Sempre que `TASK_REGISTRY.md` ou `GROUP.md` mudar, rode:

```bash
python scripts/update_workflow_dashboard.py
```

Para agentes, prefira a versão silenciosa:

```bash
python scripts/update_workflow_dashboard.py --quiet
```

No Cursor, `.cursor/hooks.json` chama esse sync automaticamente após edições, sem adicionar saída ao contexto.

## Prompt: configurar primeira task

```text
Leia TASK_REGISTRY.md, GROUP.md, LOCAL.md e docs/FRAMEWORK.md.
Sou novo neste workflow. Quero iniciar uma task da FIAP pelo fluxo portal-first.
Confira minha identidade, pergunte se e solo ou grupo e me guie sem implementar antes da SPEC.
```

## Prompt: fazer minha parte

```text
Leia GROUP.md, LOCAL.md e specs/<task>/SPLIT.md.
Quero fazer apenas minha parte.
Identifique minha responsabilidade, limite o escopo e me diga quais arquivos devo tocar.
```

## Prompt: revisar ou integrar

```text
Leia SPEC.md, WORKPLAN.md, SPLIT.md, INTEGRATION.md e REVIEW.md da task.
Quero revisar/integrar o trabalho do grupo.
Liste riscos, conflitos, pendencias humanas e quality gates antes da entrega.
```

## Decisoes que o colega precisa saber

- `LOCAL.md` e pessoal e nao deve ir para o Git.
- `GROUP.md` e compartilhado e deve refletir os membros reais.
- Toda task deve nascer de fonte oficial do portal ou de captura manual documentada.
- Entrega final no portal FIAP continua sendo acao humana.
- Credenciais, cookies, prints sensiveis e PDFs autenticados nao devem ser publicados sem revisao.

## Checklist de sucesso

- [ ] `LOCAL.md` existe e identifica o aluno.
- [ ] `GROUP.md` tem grupo, turma e membros.
- [ ] `docs/dashboard/index.html` abre e mostra o estado atual.
- [ ] O aluno sabe pedir task solo, minha parte, revisao e integracao.
- [ ] O aluno sabe onde ficam `specs/`, `tasks/` e `knowledge/`.
- [ ] Automacao FIAP foi configurada ou fallback manual foi entendido.

## Proximo passo

Depois do onboarding, seguir [`09-task-portal-first.md`](09-task-portal-first.md) para tasks oficiais ou [`10-study-pack-generation.md`](10-study-pack-generation.md) para estudo.
