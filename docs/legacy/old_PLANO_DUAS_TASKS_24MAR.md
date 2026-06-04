# Plano de Ação Final — 2 entregas em 24/03/2026

## Janelas úteis

| Bloco | Horário | Duração |
|-------|---------|---------|
| **Hoje (23/03)** | 23:10 → 02:00 | **2h50** |
| **Amanhã (24/03)** | 19:10 → 23:40 (10 min buffer upload) | **4h30** |
| **TOTAL** | | **7h20** |

---

## Status AGORA (23/03 ~23:00)

### Task 1 — FarmTech (o que falta)
| Item | Status |
|------|--------|
| Código (Python + R) | PRONTO |
| `resumo_artigo.pdf` | **PRONTO** (recém-gerado, Arial 11, margens 2cm) |
| `link_video.txt` | falta link real |
| Vídeo (~5 min) | **falta gravar** |
| YouTube upload | falta |
| GitHub push | falta (se exigido) |
| ZIP final | falta |

### Task 2 — Teachable Machine (o que falta)
| Item | Status |
|------|--------|
| Imagens (3 classes) | falta |
| Teachable Machine (treino + teste) | falta |
| Prints | falta |
| Relatório PDF | **esqueleto pronto** (só preencher [COLAR]) |

---

## HOJE 23/03 — 23:10 até 02:00 (2h50)

**Foco: Task 2 (imagens + Teachable Machine + prints)**

### 23:10 → 23:40 (30 min) — IMAGENS

**Atalho**: baixar do **Pexels** (pexels.com) — é mais rápido que fotografar.

Abrir no browser:
- `pexels.com` → buscar em inglês → baixar direto (sem conta).

| Classe | Busca no Pexels | Meta |
|--------|-----------------|------|
| **Talheres** | `fork knife spoon cutlery` | **15 treino** + **4 teste** |
| **Panelas** | `cooking pot pan kitchen` | **15 treino** + **4 teste** |
| **Utensílios de preparo** | `spatula ladle kitchen utensil whisk` | **15 treino** + **4 teste** |

Salvar em:
```
C:\Users\higor\Downloads\task2_imagens\
  talheres_treino\    (15 fotos)
  panelas_treino\     (15 fotos)
  preparo_treino\     (15 fotos)
  talheres_teste\     (4 fotos)
  panelas_teste\      (4 fotos)
  preparo_teste\      (4 fotos)
```

**Dica**: baixar tamanho médio (1280px), não precisa 4K.  
**IMPORTANTE**: imagens de **teste** devem ser **diferentes** das de treino.

---

### 23:40 → 00:40 (60 min) — TEACHABLE MACHINE

1. Abrir https://teachablemachine.withgoogle.com
2. **Image Project** → **Standard image model**
3. Renomear classes: `Talheres`, `Panelas`, `Utensilios de Preparo`
4. Upload das pastas `*_treino` em cada classe
5. **PRINT 1**: tela com as 3 classes e amostras visíveis

**Treino 1 (baseline)**:
- Clicar **Train Model** com padrão
- Anotar: `Epochs: ?, Batch size: ?, Learning rate: ?` (ver em Advanced antes de treinar)
- **PRINT 2**: tela pós-treino (acurácia/loss se visível)

**Treino 2 (ajuste)**:
- Em **Advanced**: mudar epochs para 100 (ou o dobro do padrão), manter o resto
- Retreinar
- **PRINT 3**: comparar resultado

---

### 00:40 → 01:10 (30 min) — TESTE + PRINTS

1. Na seção **Preview**, trocar para **File** (upload)
2. Subir uma a uma as imagens das pastas `*_teste`
3. Anotar numa tabela:

| Imagem | Classe real | Classificação do modelo | Confiança (%) | Acertou? |
|--------|------------|------------------------|--------------|----------|
| teste_talher_1.jpg | Talheres | ? | ? | ? |
| ... | ... | ... | ... | ... |

4. **PRINT 4**: tela de preview mostrando uma classificação com a barra de confiança
5. Calcular: **acertos / total = acurácia no teste**

---

### 01:10 → 01:50 (40 min) — PREENCHER RELATÓRIO

1. Abrir `task2_teachable_kitchen/RELATORIO_ESQUELETO.md` no **Google Docs** (ou Word)
2. Colar o texto inteiro
3. Substituir todos os `[COLAR]` com seus números reais
4. Inserir os 4 prints nos locais marcados `[INSERIR PRINT]`
5. Ajustar formatação básica (títulos em negrito, espaçamento)

**OU**: cola aqui no chat os números (acurácia, épocas, batch, LR, N imagens, acertos/erros) e eu gero o texto preenchido para você só colar.

---

### 01:50 → 02:00 (10 min) — EXPORTAR PDF

1. **Arquivo → Fazer download → PDF** (Google Docs) ou **Salvar como PDF** (Word)
2. Nome obrigatório: `HigorHenriqueGarcia_RM571820_fase1_cap2.pdf`
3. Abrir o PDF → conferir: nome, RM, prints visíveis, sem página em branco extra
4. **Salvar** em `task2_teachable_kitchen/` como backup
5. **DORMIR**

---

## AMANHÃ 24/03 — 19:10 até 23:40 (4h30)

### 19:10 → 19:25 (15 min) — Lanche + revisar

- Abrir os 2 PDFs e conferir.
- Se algo estiver ruim no Cap 2: corrigir agora (prioridade).

### 19:25 → 19:40 (15 min) — UPLOAD TASK 2

- Portal FIAP → Task 2 → upload `HigorHenriqueGarcia_RM571820_fase1_cap2.pdf`
- **Conferir** o arquivo no upload antes de confirmar. Não dá para trocar depois.
- **Task 2 entregue.**

### 19:40 → 20:30 (50 min) — VÍDEO TASK 1

Gravar tela + narração (pode ser microfone do headset ou celular filmando a tela):

| Minuto | O que mostrar |
|--------|---------------|
| 0:00–0:30 | Apresentação: nome, RM, projeto FarmTech |
| 0:30–2:00 | Terminal: rodar `python3 main.py`, cadastrar 1 cana + 1 café, listar, mostrar área calculada |
| 2:00–3:00 | Cadastrar 1 manejo, listar, mostrar cálculo de insumos |
| 3:00–3:30 | Exportar CSV (opção 10) |
| 3:30–4:15 | Rodar `Rscript estatistica.R`, mostrar média/desvio |
| 4:15–4:45 | Rodar `Rscript clima_estatistica.R`, mostrar dados da API |
| 4:45–5:00 | Encerramento |

**Atalho para gravar**: Windows tem **Xbox Game Bar** (`Win+G` → gravar tela) ou **OBS** se já tiver. No WSL, rode os comandos normalmente que a gravação captura o terminal.

Se a narração ficar ruim: **sem som** e texto na tela também funciona (adicione no título do terminal ou no slide).

### 20:30 → 21:00 (30 min) — YOUTUBE

1. youtube.com → Criar → Enviar vídeo
2. Título: `FarmTech Solutions - Task 1 - Higor Henrique Garcia RM571820`
3. Visibilidade: **Não listado**
4. Enquanto processa: prosseguir com próximo passo

### 21:00 → 21:15 (15 min) — FINALIZAR TASK 1

No Cursor/terminal:
```bash
cd ~/fiap_squad_deliverables

# Colar link do YouTube no arquivo (substituir URL_AQUI)
echo "Link do vídeo no YouTube (não listado):" > task1_farmtech/link_video.txt
echo "URL_AQUI" >> task1_farmtech/link_video.txt

# Gerar ZIP
zip -r task1_farmtech_WOLF.zip task1_farmtech/ \
  -x "task1_farmtech/__pycache__/*" \
  -x "task1_farmtech/**/*.pyc" \
  -x "task1_farmtech/gerar_pdf_resumo.py" \
  -x "task1_farmtech/fonts/*"
```

Verificar conteúdo do ZIP:
```bash
unzip -l task1_farmtech_WOLF.zip
```

Deve conter: `main.py`, `culturas.py`, `estatistica.R`, `clima_estatistica.R`, `resumo_artigo.pdf`, `resumo_artigo.txt`, `link_video.txt`, `MANUAL_ENTREGA.md`.

### 21:15 → 21:30 (15 min) — GITHUB (se necessário)

No browser: github.com → New repository → `fiap-task1-farmtech` → **Public** → **não** inicializar com README.

No terminal:
```bash
cd ~/fiap_squad_deliverables
git remote add origin https://github.com/SEU_USUARIO/fiap-task1-farmtech.git
git push -u origin master
```

### 21:30 → 21:45 (15 min) — UPLOAD TASK 1

- Portal FIAP → Task 1 → upload (ZIP? link GitHub? o que a plataforma pedir)
- **Conferir** antes de confirmar.

### 21:45 — **TUDO ENTREGUE**

Buffer de **~2h** antes do prazo. Use para:
- Respirar
- Conferir se os uploads foram confirmados na plataforma
- Atualizar `TASK_REGISTRY.md` com status CONCLUÍDA

---

## Resumo visual

```
HOJE 23/03
  23:10 ████████ Imagens (Pexels)
  23:40 ████████████████ Teachable Machine (treino x2)
  00:40 ████████ Teste + prints
  01:10 ██████████ Preencher relatório
  01:50 ██ Exportar PDF Cap 2
  02:00 💤 DORMIR

AMANHÃ 24/03
  19:10 ██ Revisar PDFs
  19:25 ██ UPLOAD TASK 2 ✓
  19:40 ██████████ Gravar vídeo Task 1
  20:30 ██████ YouTube upload
  21:00 ██ ZIP + link_video.txt
  21:15 ██ GitHub (se precisar)
  21:30 ██ UPLOAD TASK 1 ✓
  21:45 🎉 ENTREGUE — 2h de buffer
```
