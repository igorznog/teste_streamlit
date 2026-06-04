# Preparar entrega — o que já está feito vs. amanhã

> Atualizado em **17/05/2026 ~20:50**. Vídeo e portal ficam para você.

## ✅ Feito automaticamente (hoje)

| Item | Onde |
|------|------|
| Dataset 1000 linhas | `dados/leituras_sensores.csv` |
| DDL + 10 queries SQL | `sql/` |
| Dashboard Streamlit | `dashboard/app.py` |
| **5 prints dashboard** | `prints/dash_01_home.png` … `dash_05_chuva_prevista.png` |
| **6 prints SQL** (validação local) | `prints/sql_q*.png`, `prints/09_count_query.png`, `prints/10_select_all.png` |
| Notebook ML (Cap 10) | `ml/AlunoProductOwner_RM000000_fase3_cap10.ipynb` |
| README + MANUAL + SPEC | raiz do projeto |
| Venv com deps | `.venv/` (não commitar) |

## ⏳ Amanhã (você — ~2h)

### 1. Oracle no servidor FIAP (~20 min)

No PowerShell ou bash (senha = data nascimento **DDMMYY**, 6 dígitos):

```bash
cd tasks/task06_fase3_cap1_oracle
export FIAP_ORACLE_PASSWORD='XXXXXX'   # não commitar
.venv/bin/python scripts/oracle_carga_fiap.py
```

Isso cria a tabela real no `oracle.fiap.com.br` e gera `prints/oracle_auto/*.html`.
Abra cada HTML e tire print (ou use no vídeo).

**Opcional (mais fiel ao enunciado):** instalar SQL Developer no Windows e seguir
`sql/02_importar_csv.md` — substitui `prints/01_*.png` … `prints/10_*.png`.

### 2. Vídeo (~1h30)

Roteiro em `MANUAL_ENTREGA.md` bloco E. Colar URL em `link_video.txt`.

### 3. GitHub (~15 min)

```bash
cd tasks/task06_fase3_cap1_oracle
gh auth login
gh repo create farmtech-fase3-cap1 --public --source=. --remote=origin
git init && git add -A && git commit -m "feat: entrega Cap 1 Fase 3 (Oracle + Dashboard + ML)"
git branch -M main && git push -u origin main
```

Atualizar link do repo no `README.md`.

### 4. Portal FIAP (~15 min)

1. Cap 10: <https://on.fiap.com.br/mod/EXEMPLO/view.php?id=000000> → **Entregar** (notebook).
2. Cap 1: <https://on.fiap.com.br/mod/EXEMPLO/view.php?id=000000> → **Trazer Grupo Anterior** → links GitHub + vídeo → **Entregar**.

## Checklist rápido

- [ ] `FIAP_ORACLE_PASSWORD` rodou sem erro
- [ ] Vídeo no YouTube (não listado) + `link_video.txt`
- [ ] Repo `farmtech-fase3-cap1` no GitHub
- [ ] Cap 10 submetido no portal
- [ ] Cap 1 submetido no portal
- [ ] Print `prints/portal_entrega_confirmada.png`
