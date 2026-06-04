# Knowledge Base — WOLF Squad

Base de conhecimento organizada por disciplina. Contém pílulas de estudo e flashcards gerados a partir do conteúdo das aulas da FIAP.

## Estrutura

```
knowledge/
  disciplina_nome/
    _meta.md                ← resumo da disciplina, professor, formato da prova
    aula01_tema.md          ← pílula de conhecimento
    aula02_tema.md
    flashcards.md           ← perguntas e respostas para revisão
```

## Formato da pílula (`aulaNN_tema.md`)

```markdown
# [Título do Tema]
**Disciplina**: X | **Aula**: N | **Data**: YYYY-MM-DD

## Conceito-chave
[1-3 frases que explicam o essencial]

## Como funciona
[Explicação com exemplo prático, sem enrolação]

## Código/Exemplo
[Se aplicável — snippet funcional]

## Pegadinhas de prova
- [Erro comum 1]
- [Erro comum 2]

## Conexões
- Relacionado a: [link para outra pílula]
```

## Formato dos flashcards (`flashcards.md`)

```markdown
# Flashcards — [Disciplina]

### Q1
**P:** [Pergunta]
**R:** [Resposta concisa]
```

## Como usar

**No Cursor**: peça "me quizze sobre [disciplina]" ou "resuma o conteúdo de [disciplina]".

**No celular**: sincronize esta pasta com Google Drive e peça ao Gemini para quizzar sobre o conteúdo dos arquivos.
