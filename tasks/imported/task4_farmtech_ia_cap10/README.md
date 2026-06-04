# FarmTech Solutions — Modelagem de IA
## FIAP IA 2026/1 | Fase 3 — Cap 10 | Grupo 45

**Alunos:** Vinicius Anjos (RM572814) · Higor Henrique Garcia (RM571820) · Igor (RM572822) · Humberto (RM570536)  
**Repositório canônico (fork do grupo):** [higorhg/fiap-ia-fase3-grupo45](https://github.com/higorhg/fiap-ia-fase3-grupo45)  
**Prazo:** 19/05/2026

---

## Sobre o Projeto

Análise exploratória e modelagem preditiva com o dataset `produtos_agricolas.csv`.
O objetivo é recomendar a cultura agrícola ideal com base em condições de solo e clima.

## Estrutura do Repositório

```
fiap-ia-fase3-grupo45/
├── produtos_agricolas.csv                  # Dataset principal
├── parte1_exploracao_VINICIUS.ipynb        # Vinicius
├── parte2_descritiva_HIGOR.ipynb           # Higor
├── parte3_perfil_IGOR.ipynb               # Igor
├── parte4_modelos_HUMBERTO.ipynb          # Humberto
├── HigorHenriqueGarcia_RM571820_fase3_cap10.ipynb  # Entrega final consolidada
├── graficos/                              # PNGs gerados pelo notebook final
├── gerar_notebook_final.py                # Script reprodutível para regenerar a entrega
├── referencia_notebook_completo.ipynb      # Referência (não editar)
└── README.md
```

## Divisão do Trabalho

| Parte | Responsável | Conteúdo |
|---|---|---|
| 1 | Vinicius | Carregamento + Análise Exploratória (gráficos 1-2) |
| 2 | Higor | Correlação + Análise Descritiva + Achados (gráficos 3-5) |
| 3 | Igor | Perfil Ideal + Comparação de 3 Culturas (gráfico 6) |
| 4 | Humberto | 5 Modelos Preditivos + Comparação + Conclusões (gráficos 7-9) |

## Entrega Final Consolidada

Arquivo principal para submissão:

```text
HigorHenriqueGarcia_RM571820_fase3_cap10.ipynb
```

Este notebook integra as partes do grupo em uma entrega única e executável:

- análise exploratória e descritiva com 10 gráficos;
- perfil ideal de solo/clima e comparação de 3 culturas (`rice`, `coffee`, `banana`);
- 5 modelos preditivos com algoritmos diferentes;
- comparação por `accuracy` e `f1_macro`;
- matriz de confusão do melhor modelo;
- importância das variáveis e conclusões.

As imagens dos gráficos também são salvas automaticamente em `graficos/`.

O texto final foi reescrito como uma narrativa única do Grupo 45, com rastreabilidade das branches usadas,
decisões próprias de análise e conclusões específicas sobre os resultados do dataset.

### Rastreabilidade da integração

- Parte 1: completada no notebook final a partir da estrutura local.
- Parte 2: notebook de Higor usado como base da análise descritiva.
- Parte 3: branch `origin/parte3-igor` usada como insumo para o perfil ideal.
- Parte 4: branch `origin/humberto` usada como insumo para os modelos e conclusões.
- `referencia_notebook_completo.ipynb`: usada como referência de organização, sem edição direta.

## Fluxo de trabalho (3 cenários)

O grupo pode operar de três formas; o Git é o mesmo nos três casos.

| Cenário | Quando usar | O que fazer |
|--------|----------------|-------------|
| **A — Só a sua parte** | O enunciado ou o líder já definiu o recorte (ex.: Parte 2) | Clone o repo, crie a branch da parte (`parte2-higor`), edite **apenas** o notebook da sua parte, abra PR para `main`. |
| **B — Task inteira em grupo** | Todos entregam um único artefato conjunto | Um repo (este), divisão por notebook ou por pastas; cada pessoa na sua branch; integração na `main` via PR após revisão. |
| **C — Task inteira sozinho** | Atividade individual na FIAP | Trabalhe na `main` ou em uma branch única; não precisa dividir notebooks — ignore a coluna “Responsável” e use o `referencia_notebook_completo.ipynb` só como consulta. |

**Integração das partes dos outros:** cada membro faz `git push` da própria branch; o dono do fork (Higor) ou qualquer membro com permissão abre **Pull Request** no GitHub para `main`, resolve conflitos (quase sempre só em `README.md`), faz *merge* e os demais atualizam com `git checkout main && git pull`.

## Git Workflow (branches + PR)

```bash
# 1. Clone o repositório canônico do grupo
git clone https://github.com/higorhg/fiap-ia-fase3-grupo45.git
cd fiap-ia-fase3-grupo45

# 2. Atualize a main e crie sua branch
git checkout main
git pull origin main
git checkout -b parte1-vinicius   # ou parte2-higor | parte3-igor | parte4-humberto

# 3. Trabalhe no seu notebook (um arquivo por pessoa reduz conflito)

# 4. Commit e push da branch
git add seu_notebook.ipynb
git commit -m "feat: parte X concluída"
git push -u origin parte1-vinicius

# 5. No GitHub: Pull Request → main → merge após revisão do grupo
```

**Convenção de branches:** `parte{n}-{nome_curto}` em minúsculas, alinhado ao arquivo (`parte2-higor`, etc.).

## Como Rodar

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook
```

Abra os notebooks a partir da pasta do repositório para o CSV ser encontrado automaticamente.

Para regenerar e executar a entrega final:

```bash
source .venv/bin/activate
python gerar_notebook_final.py
jupyter nbconvert --to notebook --execute --inplace HigorHenriqueGarcia_RM571820_fase3_cap10.ipynb --ExecutePreprocessor.timeout=300
```
