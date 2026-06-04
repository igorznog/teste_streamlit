# Integracao NotebookLM

Use quando o aluno quiser estudar pelo NotebookLM com fontes limpas geradas pelo workflow.

## Veredito pratico

Para o NotebookLM comum, o caminho mais confiavel e gerar um pacote de fontes e importar manualmente via Google Drive/NotebookLM.

A API oficial e voltada ao NotebookLM Enterprise/Google Cloud. Qualquer automacao nao oficial deve ser tratada como experimental e opcional.

## Fluxo recomendado

1. Capturar fontes oficiais do portal FIAP.
2. Gerar study pack com `docs/workflows/10-study-pack-generation.md`.
3. Exportar somente fontes seguras:

```bash
python scripts/export_notebooklm_pack.py \
  --source knowledge/fase3_overview \
  --source specs/task06_fase3_cap1_oracle \
  --dest ~/FIAP_NotebookLM/fase3_cap1
```

4. Revisar o `00_INDEX.md` gerado.
5. Subir a pasta para Google Drive.
6. Criar um notebook no NotebookLM e adicionar as fontes.

## O que exportar

- Pílulas em Markdown.
- `00_INDEX.md` de study packs.
- Cornell/Feynman/quiz bank/defesa oral.
- Specs e rubricas sem dados sensiveis.
- Flashcards.
- Resumos de entregas.

## O que nao exportar por padrao

- Senhas, cookies, `.env`, tokens.
- Prints autenticados do portal.
- Capturas brutas em `docs/validation/captures/`.
- PDFs do portal se houver risco de copyright fora do uso pessoal.
- Notebooks com RM real, emails ou dados pessoais sem revisao.

## CLI-Anything

O `CLI-Anything` pode ser investigado como modo experimental para operar o NotebookLM comum por automacao de UI, mas nao deve virar dependencia obrigatoria do framework.

Use somente quando:

- o aluno entende que e automacao nao oficial;
- nao houver credenciais no repositorio;
- houver revisao manual antes de publicar ou compartilhar;
- o fluxo manual por Drive nao for suficiente.

## Enterprise/API

Se a turma ou empresa tiver NotebookLM Enterprise, registrar:

- projeto Google Cloud;
- escopo de autenticacao;
- politica de dados;
- quem pode criar notebooks;
- onde os arquivos ficam armazenados.

Sem isso, manter o modo comum por Drive.

## Prompt para a IA

```text
Leia docs/integrations/notebooklm.md e docs/workflows/10-study-pack-generation.md.
Gere um pacote NotebookLM seguro a partir das fontes da task/capitulo.
Nao exporte credenciais, capturas autenticadas brutas, PDFs restritos ou dados pessoais sem me avisar.
```
