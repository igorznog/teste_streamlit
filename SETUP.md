# Setup em 5 minutos — integração de colegas

Guia curto para **qualquer pessoa do grupo** clonar o repo, alinhar com a IA e começar uma task sem depender de combinados soltos.

---

## 1. Clonar e abrir

```bash
git clone <URL_DO_REPO_DO_GRUPO>.git
cd <pasta-do-repo>
```

Abre a pasta no **Cursor**, **VS Code** ou outro IDE.

Se esta for a primeira vez no projeto, depois do setup leia tambem [`docs/workflows/00-onboarding-colega.md`](docs/workflows/00-onboarding-colega.md).

---

## 2. Rodar o setup interativo

```bash
python setup.py
```

O script:

- detecta sistema, Python, Git, branch e remote;
- pergunta teu nome, RM opcional, GitHub e IDE;
- cria `LOCAL.md` para este clone;
- pergunta se o uso é solo ou em grupo;
- pode atualizar `GROUP.md` com membros e responsabilidades;
- mostra os próximos comandos Git.

> O setup não faz push, não grava senha e não acessa o portal FIAP.

Para ver o estado atual do grupo de forma visual, abra depois:

```text
docs/dashboard/index.html
```

Se você atualizar `TASK_REGISTRY.md` ou `GROUP.md`, regenere os painéis:

```bash
python scripts/update_workflow_dashboard.py
```

No Cursor isso também roda por hook silencioso depois de edições. Em outros agentes, peça:

```bash
python scripts/update_workflow_dashboard.py --quiet
```

---

## 3. Identificar o grupo (todos veem o mesmo)

Edita o ficheiro **[`GROUP.md`](GROUP.md)** na raiz (commitado no Git):

- Nome da disciplina / fase
- **Número ou nome do grupo** (ex.: Grupo EXEMPLO)
- Tabela com **todos os membros**: nome, RM (opcional), GitHub, partes do trabalho

Assim o projeto fica **reconhecível** e a IA sabe **quem são os colegas** e a divisão de tarefas.

> Um membro pode preencher na primeira vez; os outros fazem `git pull` e completam a sua linha se faltar.

---

## 4. Quem está neste PC (só tua máquina)

Se preferires fazer manualmente em vez de usar `python setup.py`, copia o exemplo:

```bash
cp LOCAL.example.md LOCAL.md
```

Edita **`LOCAL.md`** com **o teu nome** (e RM se quiseres).  
Este ficheiro **não vai para o Git** (cada colega tem o seu).

A IA usa **`GROUP.md`** (equipa inteira) + **`LOCAL.md`** (tu neste clone) para dirigir-se a ti corretamente.

---

## 5. O teu nome nas regras do Cursor (opcional)

Se usas **Cursor**, abre [`.cursorrules`](.cursorrules) e substitui **`{{ALUNO}}`** pelo teu nome (uma linha no início).

Noutros IDEs isso não é lido automaticamente — o passo 3 (`LOCAL.md`) + anexar [`docs/FRAMEWORK.md`](docs/FRAMEWORK.md) no chat cobre o mesmo efeito.

---

## 5.1 Login automático no portal FIAP (opcional, mas recomendado)

Quer que o assistente abra páginas do portal FIAP sozinho (capturar enunciado, ler aula, tirar screenshot)?

Rode UM comando:

```bash
bash scripts/setup_fiap_automation.sh
```

O script é interativo, em português, e cuida de tudo (Node, agent-browser, Chrome, skill, vault de senha). Leva 3–5 minutos.

Documentação curta: [`docs/QUICKSTART_AUTOMACAO.md`](docs/QUICKSTART_AUTOMACAO.md).
Documentação completa: [`docs/integrations/agent-browser-fiap.md`](docs/integrations/agent-browser-fiap.md).

Pode pular este passo agora e voltar depois — todo o resto do framework funciona sem isso.

---

## 6. Primeira conversa com a IA

Diz explicitamente na primeira mensagem (ou anexa ficheiros):

- `TASK_REGISTRY.md`
- `GROUP.md`
- `LOCAL.md` (se existir)
- `docs/FRAMEWORK.md` (se o assistente não tiver contexto do repo)

Exemplo geral:

> Somos o Grupo XX da FIAP. Lê `GROUP.md`, `LOCAL.md` e `TASK_REGISTRY.md` e ajuda-me na Parte Y.

Exemplo para colega novo:

```text
Leia TASK_REGISTRY.md, GROUP.md, LOCAL.md, docs/FRAMEWORK.md
e docs/workflows/00-onboarding-colega.md.
Sou novo neste workflow. Confirme se minha identidade e grupo estao configurados
e me diga o proximo passo para iniciar uma task oficial da FIAP.
```

---

## 7. Operar o fluxo no dia a dia

### Quando receber uma task/challenge

Use primeiro a fonte oficial do portal. Se a automacao estiver configurada, envie a URL; se nao estiver, cole a captura manual completa.

```text
Leia GROUP.md, LOCAL.md, TASK_REGISTRY.md, docs/FRAMEWORK.md
e docs/workflows/09-task-portal-first.md.
Vou iniciar uma task oficial da FIAP.
Use a URL/captura abaixo como fonte oficial, classifique o tipo de entrega,
pergunte se e solo ou grupo, crie SPEC.md e WORKPLAN.md antes de implementar.

[cole aqui a URL, captura automatica ou enunciado completo]
```

Se você só vai fazer sua parte:

```text
Quero fazer apenas minha parte nesta task.
Leia GROUP.md, LOCAL.md e specs/<task>/SPLIT.md.
Identifique minha responsabilidade, limite o escopo a ela e me guie até abrir PR.
```

### Quando receber uma aula

O framework aceita dois jeitos:

1. **PDF da aula:** anexe o PDF no chat e peça ingestão.
2. **Página da aula:** selecione o conteúdo no navegador, use `Ctrl+C` e cole no chat.

Prompt recomendado:

```text
Leia docs/workflows/01-ingestao-aula.md.
Vou enviar uma aula da FIAP por PDF ou texto copiado.
Crie uma pílula em knowledge/<disciplina>/,
atualize flashcards.md,
registre conexões com tasks e me explique como estudar esse conteúdo.

[anexe o PDF ou cole o texto da aula]
```

### Quando quiser estudar ou defender uma entrega

```text
Leia docs/workflows/10-study-pack-generation.md.
Use as fontes oficiais ja capturadas para criar um study pack em knowledge/:
pilula, Cornell, Feynman, mapa conceitual, quiz bank, flashcards,
defesa oral e plano SRS D+1/D+3/D+7.
```

Para NotebookLM:

```bash
python scripts/export_notebooklm_pack.py --source knowledge/<disciplina> --dest ~/FIAP_NotebookLM/<tema>
```

Depois revise o `00_INDEX.md` gerado e importe manualmente no NotebookLM comum via Google Drive.

### Quando precisar integrar o grupo

```text
Leia SPEC.md, SPLIT.md, WORKPLAN.md, INTEGRATION.md e REVIEW.md da task.
Quero integrar as partes do grupo.
Liste PRs/branches esperadas, ordem de merge, conflitos prováveis e checklist final.
```

---

## Onde ir depois

| Ficheiro | Para quê |
|----------|----------|
| [`README.md`](README.md) | Visão geral, IDEs, Git, sync `knowledge/` |
| [`docs/FRAMEWORK.md`](docs/FRAMEWORK.md) | Contrato completo agnóstico de IDE |
| [`TASK_REGISTRY.md`](TASK_REGISTRY.md) | Tasks e checklists |
| [`GROUP.md`](GROUP.md) | Identificação do grupo e membros |
| [`LOCAL.md`](LOCAL.md) | Só no teu PC (criar a partir de `LOCAL.example.md`) |
| [`docs/dashboard/index.html`](docs/dashboard/index.html) | Painel visual central do workflow |
| [`docs/dashboard/registry.html`](docs/dashboard/registry.html) | Task registry visual com filtros |
| [`docs/workflows/00-onboarding-colega.md`](docs/workflows/00-onboarding-colega.md) | Jornada guiada para colega novo |
| [`docs/workflows/09-task-portal-first.md`](docs/workflows/09-task-portal-first.md) | Comecar task pela fonte oficial |
| [`docs/workflows/10-study-pack-generation.md`](docs/workflows/10-study-pack-generation.md) | Gerar estudo moderno e defesa |
| [`docs/templates/FIAP_DELIVERY_TYPES.md`](docs/templates/FIAP_DELIVERY_TYPES.md) | Matriz de entregaveis FIAP |
| [`docs/templates/SAFETY_PII_COPYRIGHT_CHECKLIST.md`](docs/templates/SAFETY_PII_COPYRIGHT_CHECKLIST.md) | Revisao antes de publicar/exportar |
