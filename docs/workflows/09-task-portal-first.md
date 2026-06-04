# Workflow 09 — Task portal-first

Use para qualquer task, challenge, quiz ou entrega cuja fonte oficial esteja no portal FIAP.

## Objetivo

Garantir que a execucao nasce da fonte oficial, nao de memoria ou conversa solta.

## Entradas

- URL da pagina FIAP, quando disponivel.
- Captura automatica em `docs/validation/captures/`, quando possivel.
- Captura manual pelo template `docs/templates/FIAP_TASK_CAPTURE_TEMPLATE.md`, quando necessario.
- `GROUP.md`, `LOCAL.md` e `TASK_REGISTRY.md`.

## Fluxo

1. Ler `TASK_REGISTRY.md`, `GROUP.md` e `LOCAL.md`.
2. Capturar a pagina oficial:
   - preferir `agent-browser` e a skill `fiap-portal-capture`;
   - usar PDF/Ebook como fonte de aula quando o capitulo tiver esse recurso;
   - capturar pagina de entrega para rubrica, prazo, status, anexos e disclaimers;
   - se a automacao falhar, usar captura manual pelo template.
3. Identificar o tipo de entrega com `docs/templates/FIAP_DELIVERY_TYPES.md`.
4. Extrair requisitos obrigatorios, opcionais, "ir alem", prazo e formato de upload.
5. Perguntar se a task e solo ou em grupo.
6. Se for grupo, perguntar o papel atual do aluno: coordenar, fazer parte, revisar, assumir ou integrar.
7. Criar ou atualizar `specs/taskNN_nome/SPEC.md`.
8. Criar `WORKPLAN.md`.
9. Se for grupo, criar `SPLIT.md` e `INTEGRATION.md`.
10. Criar uma secao de defesa: perguntas provaveis, pontos tecnicos e relacao com aulas.
11. So implementar depois de o Product Owner aprovar o escopo.
12. Ao final, atualizar `REVIEW.md`, `TASK_REGISTRY.md` e pendencias humanas.

## Saidas esperadas

- `specs/taskNN_nome/SPEC.md`
- `specs/taskNN_nome/WORKPLAN.md`
- `specs/taskNN_nome/SPLIT.md` e `INTEGRATION.md` se grupo
- `specs/taskNN_nome/REVIEW.md` antes da entrega
- artefatos em `tasks/taskNN_nome/`
- estudo relacionado em `knowledge/<disciplina>/`, quando fizer sentido

## Prompt recomendado

```text
Leia docs/workflows/09-task-portal-first.md.
Use a fonte oficial do portal FIAP para iniciar esta task.
Capture ou aceite minha captura manual, extraia requisitos, identifique o tipo de entrega,
pergunte solo/grupo e crie SPEC.md + WORKPLAN.md antes de implementar.

[URL ou captura da pagina]
```

## Checklist portal-first

- [ ] URL ou captura manual registrada.
- [ ] Prazo e status de submissao registrados.
- [ ] Rubrica e anexos preservados.
- [ ] Tipo de entrega classificado.
- [ ] Modo solo/grupo definido.
- [ ] Responsabilidade do aluno clara.
- [ ] SPEC e WORKPLAN criados antes da execucao.
- [ ] Safety review previsto antes de publicar/exportar.
