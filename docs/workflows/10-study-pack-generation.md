# Workflow 10 — Geracao de study pack

Use quando o aluno quiser estudar um capitulo, preparar quiz/fast test, defender uma entrega ou exportar fontes para NotebookLM.

## Objetivo

Transformar fontes oficiais em um pacote de estudo com active recall, revisao espacada, explicacao Feynman, mapa conceitual e defesa oral.

## Entradas

- PDF/Ebook capturado do portal FIAP.
- Pagina HTML capturada do portal, quando necessario.
- `SPEC.md` e rubrica da task, se houver entrega relacionada.
- Materiais ja existentes em `knowledge/<disciplina>/`.

## Saida padrao

Criar uma pasta:

```text
knowledge/<disciplina>/study_packs/<fase-ou-capitulo>/
```

Com estes arquivos:

- `00_INDEX.md`
- `lesson-note.md`
- `cornell-note.md`
- `feynman-note.md`
- `concept-map.md`
- `quiz-bank.md`
- `flashcards.md`
- `oral-defense.md`
- `srs-review-plan.md`

## Passo a passo

1. Ler `TASK_REGISTRY.md`, `GROUP.md`, `LOCAL.md` e a fonte oficial.
2. Confirmar se o objetivo e prova, task, defesa, quiz ou revisao geral.
3. Criar `00_INDEX.md` com fontes, ordem de leitura e links internos.
4. Criar a pilula principal a partir de `docs/templates/lesson-note.md`.
5. Criar Cornell note, Feynman note e concept map.
6. Gerar perguntas em `quiz-bank.md` e flashcards.
7. Gerar `oral-defense.md` quando houver entrega relacionada.
8. Criar `srs-review-plan.md` com D+1, D+3, D+7 e D+14.
9. Registrar lacunas e conexoes com tasks em `_meta.md`.
10. Se o aluno quiser NotebookLM, rodar `scripts/export_notebooklm_pack.py`.

## Prompt recomendado

```text
Leia docs/workflows/10-study-pack-generation.md.
Use as fontes oficiais capturadas para gerar um study pack moderno em knowledge/.
Inclua Cornell, Feynman, mapa conceitual, quiz bank, flashcards, defesa oral e plano SRS.
Relacione com tasks e provas da FIAP.
```

## Quality gate

- [ ] A fonte oficial esta citada.
- [ ] O pacote diferencia resumo, perguntas, defesa e revisao.
- [ ] Perguntas exigem recuperacao ativa, nao so reconhecimento.
- [ ] Lacunas ficam visiveis.
- [ ] Conteudo sensivel nao e exportado para fora do workspace sem revisao.
