# Validação do fiap-academic-workflow — Higor

## Objetivo

Usar este clone como workspace principal para próximas entregas FIAP e verificar se o fluxo funciona para o Higor e para os colegas.

## Estrutura montada

- `GROUP.md`: identificação do grupo (número a definir), RMs e responsabilidades recorrentes.
- `LOCAL.md`: identidade local do Higor neste clone. Não deve ser commitado.
- `TASK_REGISTRY.md`: histórico importado + checklist de validação.
- `knowledge/`: aulas e flashcards migrados do workflow antigo.
- `tasks/imported/`: entregas antigas copiadas quase completas, sem `.git`, `.venv`, caches e checkpoints.
- `specs/imported/`: specs retrospectivas para a Task 4 e para esta validação.
- `docs/legacy/`: registry e plano antigos preservados para consulta.

## Teste 1 — Nova conversa no Cursor

Abra `~/fiap-academic-workflow` no Cursor e envie:

```text
Leia TASK_REGISTRY.md, GROUP.md e LOCAL.md.
Me diga quem sou eu neste clone, quais tasks históricas foram importadas e qual é o próximo passo recomendado para validar o workflow com o grupo.
```

Resultado esperado: a IA identifica Higor RM571820, dados do grupo em `GROUP.md`, tasks importadas e a necessidade de criar spec antes de executar task nova.

## Teste 2 — Ingestão de aula

Cole um trecho de aula e envie:

```text
Leia docs/workflows/01-ingestao-aula.md.
Transforme este conteúdo em pílula de conhecimento e flashcards.
[cole o conteúdo]
```

Resultado esperado: arquivo novo em `knowledge/<disciplina>/` e atualização de flashcards.

## Teste 3 — Task em grupo

Cole um enunciado futuro e envie:

```text
Esta task é em grupo. Use GROUP.md e LOCAL.md para identificar quem sou eu.
Crie SPEC.md, SPLIT.md, WORKPLAN.md e INTEGRATION.md antes de implementar.
[cole o enunciado]
```

Resultado esperado: arquivos em `specs/taskNN_nome/` antes de qualquer código.

## Teste 4 — Onboarding de colega

Peça para um colega clonar/forkar o repo e preencher:

1. `GROUP.md`, se houver mudança no grupo.
2. `LOCAL.md`, copiado de `LOCAL.example.md`.
3. Primeira mensagem ao assistente lendo `TASK_REGISTRY.md`, `GROUP.md` e `LOCAL.md`.

Resultado esperado: a IA limita respostas e execução à identidade do colega naquele clone.

## Decisão após validação

- Se os testes passarem, usar este workflow como base para próximas tasks.
- Se houver ruído demais nas tasks importadas, mover parte de `tasks/imported/` para um backup local e manter só `knowledge/` + specs.
- Só commitar/pushar materiais importados depois de decidir se eles podem ficar públicos.
