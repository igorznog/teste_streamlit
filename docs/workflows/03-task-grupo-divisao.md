# Workflow 03 — Task em grupo: divisao

Use quando o grupo recebeu uma challenge/task e precisa transformar o enunciado em partes claras.

## Objetivo

Reduzir atrito: cada membro sabe sua parte, sua branch, seus arquivos e como a integracao vai acontecer.

## Entrada mais comum

O coordenador cola o enunciado completo no chat:

```text
Esta task é em grupo.
Leia GROUP.md e TASK_REGISTRY.md.
Vou colar o enunciado completo.
Crie SPEC.md, SPLIT.md, WORKPLAN.md e INTEGRATION.md.
Sugira uma divisão clara por membro, branch e entregável.

[cole aqui o enunciado completo]
```

Se a divisão já existir parcialmente:

```text
Esta é minha divisão inicial: [cole a divisão].
Valide contra o enunciado, aponte riscos e ajuste SPLIT.md.
```

## Passo a passo

1. Ler `TASK_REGISTRY.md`, `GROUP.md` e `LOCAL.md` se existir.
2. Conferir se `GROUP.md` tem membros reais e responsabilidades iniciais.
3. Ler o enunciado completo.
4. Criar `specs/taskNN_nome/SPEC.md`.
5. Criar `specs/taskNN_nome/SPLIT.md` com [`group-split.md`](../templates/group-split.md).
6. Criar `specs/taskNN_nome/WORKPLAN.md`.
7. Criar `specs/taskNN_nome/INTEGRATION.md`.
8. Atualizar `TASK_REGISTRY.md` com:
   - status da task;
   - checklist;
   - membros/partes;
   - pendencias humanas.
9. Recomendar branches para cada pessoa.

## Estrategias de divisao

- **Por arquivo:** notebooks, scripts ou secoes separados por membro.
- **Por etapa:** exploracao, modelagem, dashboard, relatorio, video.
- **Por entregavel:** codigo, docs, apresentacao, validacao.
- **Por risco:** membro mais tecnico fica com integracao/automacao; membro iniciante com parte bem delimitada e tutorial.

## Regra importante

Se duas pessoas precisarem editar o mesmo arquivo, criar uma secao de integracao explicita em `INTEGRATION.md`.

## Saidas esperadas

- `SPEC.md`
- `SPLIT.md`
- `WORKPLAN.md`
- `INTEGRATION.md`
- Branches sugeridas para cada membro
