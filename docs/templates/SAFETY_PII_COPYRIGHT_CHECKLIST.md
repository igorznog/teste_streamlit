# Checklist de seguranca, PII e copyright

Use antes de publicar repo, gerar ZIP, exportar para NotebookLM, compartilhar com colegas ou enviar material fora do portal.

## Identidade e dados pessoais

- [ ] Removi senhas, tokens, cookies, `.env` e chaves.
- [ ] Revisei emails, telefones, CPF, endereco e dados pessoais.
- [ ] RMs e nomes reais aparecem somente quando a entrega exige.
- [ ] `LOCAL.md` nao foi commitado.
- [ ] Prints nao mostram dados privados do portal, notas ou informacoes de colegas sem necessidade.

## Portal FIAP e copyright

- [ ] A fonte oficial foi usada para orientar a task.
- [ ] PDFs/e-books do portal nao foram publicados em repositorio publico sem permissao.
- [ ] Capturas autenticadas brutas ficam fora de publicacao ampla.
- [ ] Trechos da aula usados em estudo estao em formato de resumo/transformacao quando exportados.
- [ ] Links internos do portal nao expõem sessao ou tokens.

## Entrega e evidencias

- [ ] O ZIP/repo contem apenas arquivos necessarios.
- [ ] Datasets sensiveis foram anonimizados ou substituidos por sinteticos.
- [ ] Notebooks nao contem outputs com credenciais ou caminhos privados.
- [ ] Videos nao mostram senha, email institucional, notas ou tela de portal desnecessaria.
- [ ] README explica qualquer fallback usado.

## Automacao

- [ ] `agent-browser` nao inicia quiz nem submete atividade.
- [ ] CLI-Anything/NotebookLM automatizado e opcional e revisado manualmente.
- [ ] Logs grandes ou compactados foram preservados brutos quando eram evidencia.
- [ ] Se TokenJuice ou outra compactacao estiver ativa, fontes oficiais e evidencias foram conferidas sem compactacao.

## Resultado

- [ ] Seguro para entrega FIAP.
- [ ] Seguro para compartilhar com grupo.
- [ ] Seguro para publicar no GitHub, se aplicavel.
