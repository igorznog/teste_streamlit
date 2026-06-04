# Workflow 01 — Ingestao de aula

Use quando o aluno baixar um PDF, colar texto da aula, exportar conteudo do portal FIAP ou pedir para transformar uma aula em material de estudo.

## Objetivo

Transformar conteudo bruto em conhecimento reutilizavel para prova, tasks, defesa oral e study packs.

## Entradas

- PDF da aula anexado no chat.
- Texto copiado da pagina da aula com `Ctrl+C` / `Ctrl+V`.
- Conteudo extraido do portal FIAP por integracao local.
- Disciplina, fase/capitulo e data.

## Prompt recomendado

```text
Leia este workflow.
Vou enviar uma aula da FIAP por PDF ou texto copiado da pagina.
Crie uma pilula em knowledge/<disciplina>/,
atualize flashcards.md,
registre conexoes com tasks e me explique como estudar esse conteudo.

[anexe o PDF ou cole o texto da aula]
```

## Passo a passo

1. Ler `GROUP.md`, `LOCAL.md` se existir e `TASK_REGISTRY.md`.
2. Identificar disciplina, fase/capitulo, tema e fonte (PDF, copia da pagina, portal).
3. Se o texto veio de uma pagina, remover menus, rodapes, repeticoes e elementos de navegacao.
4. Criar ou atualizar pasta `knowledge/<disciplina>/`.
5. Gerar uma pilula seguindo [`docs/templates/lesson-note.md`](../templates/lesson-note.md).
6. Atualizar `knowledge/<disciplina>/flashcards.md` seguindo [`docs/templates/flashcards.md`](../templates/flashcards.md).
7. Se o aluno quiser estudo completo, seguir [`10-study-pack-generation.md`](10-study-pack-generation.md).
8. Atualizar `knowledge/<disciplina>/_meta.md` com progresso, fontes e conexoes com tasks.
9. Informar ao aluno:
   - resumo do que foi aprendido;
   - como isso pode cair em prova;
   - como isso pode ajudar em uma entrega.

## Regras

- Nao salvar credenciais ou conteudo privado indevido.
- Nao criar resumo solto fora de `knowledge/`.
- Se houver task em andamento relacionada, citar em `TASK_REGISTRY.md`.

## Saidas esperadas

- `knowledge/<disciplina>/aulaNN_tema.md`
- `knowledge/<disciplina>/flashcards.md`
- `knowledge/<disciplina>/_meta.md` atualizado
- Opcional: `knowledge/<disciplina>/study_packs/<fase-ou-capitulo>/`
