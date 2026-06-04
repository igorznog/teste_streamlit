# Matriz de tipos de entrega FIAP

Use esta matriz durante o intake para transformar a pagina oficial do portal em checklist pratico.

| Tipo | Fonte oficial a capturar | Artefatos esperados | Quality gate | Papel do aluno |
|------|--------------------------|---------------------|--------------|----------------|
| Assignment / task | Pagina `mod/assign`, rubrica, prazo, anexos | `SPEC.md`, entrega em `tasks/`, README/manual, link ou arquivo final | Conferir requisitos, rubrica, prazo e formato de upload | Confirmar escopo, executar upload final |
| Quiz / fast test | Pagina `mod/quiz`, prazo, numero de tentativas, regras | Plano de estudo, flashcards, quiz bank, checklist pre-prova | Nunca iniciar tentativa sem autorizacao; revisar conteudo relacionado | Fazer a tentativa manualmente |
| Notebook | Enunciado, dataset, rubrica, exemplos | `.ipynb`, datasets, README, prints se exigidos | Executar notebook do inicio ao fim; limpar outputs sensiveis | Conferir nome/RM/grupo e submeter |
| Dashboard | Enunciado, criterios visuais, dados | App, `requirements.txt`, README, prints, video se pedido | App roda localmente; prints mostram metricas pedidas | Gravar demonstracao e validar links |
| Oracle / SQL | Enunciado, modelo de dados, credenciais institucionais, rubrica | DDL, DML/importacao, consultas, prints, roteiro de execucao | Rodar consultas; prints evidenciam dados reais ou fallback explicado | Executar em ambiente FIAP quando necessario |
| Video | Instrucao de duracao, plataforma, conteudo minimo | Roteiro, link YouTube/Drive, arquivo auxiliar | Link acessivel; video cobre requisitos e defesa | Gravar, publicar como nao listado se apropriado |
| GitHub | Instrucao de repo, branch, arquivos exigidos | Repo, commits, README, release/ZIP se pedido | `git status` limpo; sem segredos; link publico/privado conforme enunciado | Criar repo/push quando autorizado |
| ZIP | Lista de arquivos, formato e tamanho | ZIP final, manifesto, checklist | ZIP abre e contem somente arquivos relevantes | Conferir upload correto no portal |
| Relatorio / PDF | Rubrica, formato, topicos, nomes/RMs | `.md` fonte, PDF final, referencias | Revisao ortografica, requisitos cobertos, sem PII indevida | Conferir autoria e submeter |
| Challenge em grupo | Pagina oficial, membros, regras de grupo, rubrica | `SPLIT.md`, partes individuais, `INTEGRATION.md`, entrega final | Cada parte revisada; integracao testada; pendencias humanas listadas | Coordenar, fazer parte, revisar ou integrar |
| Task solo | Pagina oficial, rubrica, prazo | `SPEC.md`, `WORKPLAN.md`, entrega final | Escopo fechado antes de implementar; teste proporcional ao risco | Validar decisao final e entregar |

## Regras de intake

- Registrar URL, prazo, status de submissao, anexos e rubrica antes de escrever codigo.
- Diferenciar requisito obrigatorio, opcional e "ir alem".
- Se a fonte oficial nao puder ser capturada automaticamente, usar `FIAP_TASK_CAPTURE_TEMPLATE.md`.
- Se a entrega for em grupo, criar `SPLIT.md` antes da execucao.
- Se houver midia de estudo ou defesa, criar tambem um roteiro em `oral-defense.md` ou `video-script.md`.

## Quality gate minimo

- [ ] Fonte oficial rastreavel.
- [ ] Entregaveis e formato de upload claros.
- [ ] Prazo registrado.
- [ ] Responsavel humano conhecido.
- [ ] Riscos de PII/copyright verificados.
- [ ] Pendencias humanas separadas das tarefas da IA.
