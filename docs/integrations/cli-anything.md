# CLI-Anything no Workflow FIAP

Use esta pagina para decidir quando vale a pena automatizar softwares externos com CLI-Anything.

## Papel no projeto

CLI-Anything e opcional. Ele pode ajudar a criar harnesses para apps que nao tem API simples, mas o workflow FIAP deve continuar funcionando sem ele.

## Bons usos

- Experimentos com NotebookLM comum quando a importacao manual por Drive for trabalhosa.
- Automacao local de ferramentas de estudo, como Zotero, LibreOffice ou OBS.
- Prototipos em que o aluno quer reduzir cliques repetitivos.

## Nao usar para

- Submeter atividades no portal FIAP.
- Iniciar quiz/fast test automaticamente.
- Manipular senhas ou cookies em arquivos do projeto.
- Substituir `agent-browser` para captura oficial do portal quando ele ja resolve o caso.

## Prioridade de automacao

1. Fonte oficial capturada por `agent-browser`.
2. Fallback manual com `FIAP_TASK_CAPTURE_TEMPLATE.md`.
3. Scripts locais do repo.
4. Integrações oficiais de APIs, se existirem.
5. CLI-Anything como experimento isolado.

## Checklist antes de usar

- [ ] Existe ganho real de tempo?
- [ ] O fluxo manual documentado continua funcionando?
- [ ] Nao ha credenciais no Git?
- [ ] A automacao nao faz submissao avaliativa?
- [ ] O aluno consegue revisar o resultado antes de publicar?

## Registro recomendado

Se um experimento der certo, documentar em `docs/validation/`:

- ferramenta automatizada;
- comando usado;
- riscos;
- limites;
- se sera promovido para workflow oficial ou mantido como opcional.
