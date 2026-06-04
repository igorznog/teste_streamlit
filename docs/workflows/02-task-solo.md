# Workflow 02 — Task solo

Use quando a atividade FIAP for individual ou quando o aluno decidir entregar sozinho.

## Objetivo

Garantir que o aluno nao pule entendimento, spec, checklist e entrega final.

## Entrada mais comum

O aluno pode simplesmente colar o enunciado completo no chat:

```text
Vou colar uma task individual da FIAP.
Leia o enunciado, extraia requisitos, crie SPEC.md e WORKPLAN.md,
e depois me guie na execução.

[cole aqui o enunciado completo]
```

## Passo a passo

1. Ler `TASK_REGISTRY.md`, `GROUP.md` e `LOCAL.md` se existir.
2. Perguntar/confirmar: “Esta task e solo?”
3. Ler o enunciado completo.
4. Criar `specs/taskNN_nome/SPEC.md` com [`task-spec.md`](../templates/task-spec.md).
5. Criar `specs/taskNN_nome/WORKPLAN.md` com [`workplan.md`](../templates/workplan.md).
6. Criar `tasks/taskNN_nome/` para os arquivos de entrega.
7. Implementar por etapas, atualizando o checklist.
8. Criar `specs/taskNN_nome/REVIEW.md` com [`review-checklist.md`](../templates/review-checklist.md).
9. Preparar entrega final: README, ZIP, video ou upload, conforme enunciado.

## Perguntas obrigatorias

- Qual o prazo?
- O que deve ser entregue?
- Precisa de video?
- Precisa de repo GitHub ou ZIP?
- Existem materiais de aula relacionados em `knowledge/`?

## Saidas esperadas

- Spec e plano em `specs/taskNN_nome/`
- Entrega em `tasks/taskNN_nome/`
- `TASK_REGISTRY.md` atualizado
