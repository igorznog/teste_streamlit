# Workflow 08 — Captura Automática de Task FIAP

## Objetivo

Converter a captura bruta da página FIAP em dados estruturados sem perder detalhes.

## Entrada esperada

- Arquivo preenchido com template: `docs/templates/FIAP_TASK_CAPTURE_TEMPLATE.md`

## Comando

```bash
python scripts/parse_fiap_task_capture.py docs/templates/FIAP_TASK_CAPTURE_TEMPLATE.md
```

## Saídas geradas

- `docs/validation/fiap_capture_parsed.json`
- `docs/validation/fiap_capture_parsed.md`

## O que o parser extrai

- Metadados (URL, disciplina/fase/cap, data/hora)
- Título da fase, janela e objetivo
- Capítulo foco
- Lista de capítulos com progresso e atividade (Fast test/How To)
- Disclaimers/avisos
- Imagens
- Links/anexos

## Fluxo recomendado

1. Login manual no portal (Brave).
2. Copiar a página com o template.
3. Rodar o parser.
4. Revisar `fiap_capture_parsed.md`.
5. Só depois gerar resumo/pílula para `knowledge/`.
