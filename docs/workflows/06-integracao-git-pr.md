# Workflow 06 — Integracao Git e Pull Requests

Modelo padrao do framework: **repo central do grupo + branch por membro/parte + PR para `main`**.

## Objetivo

Integrar trabalho em grupo com menor conflito e com rastro claro do que cada pessoa entregou.

## Fluxo para cada membro

```bash
git checkout main
git pull origin main
git checkout -b parteX-nome
# trabalhar na parte combinada
git status
git add <arquivos>
git commit -m "feat: entrega parte X"
git push -u origin parteX-nome
```

Depois abrir Pull Request para `main`.

## Checklist do PR

- [ ] Cita qual item de `SPLIT.md` foi entregue.
- [ ] Explica como validar.
- [ ] Nao inclui credenciais.
- [ ] Nao altera arquivos de colegas sem necessidade.
- [ ] Mostra pendencias conhecidas.

## Fluxo do integrador

1. Conferir `INTEGRATION.md`.
2. Revisar PRs em ordem.
3. Validar comandos/notebooks/artefatos.
4. Resolver conflitos com cuidado.
5. Atualizar README/manual final.
6. Preencher `REVIEW.md`.

## Conflitos comuns

| Arquivo | Como evitar |
|---------|-------------|
| `README.md` | Integrador edita por ultimo |
| Relatorio unico | Dividir em secoes por arquivo antes de consolidar |
| Notebook unico | Preferir um notebook por parte ou celulas claramente demarcadas |
| Dados gerados | Definir pasta `outputs/` por parte quando necessario |

## Regra de ouro

Se a integracao parecer confusa, pare e atualize `INTEGRATION.md` antes de continuar.
