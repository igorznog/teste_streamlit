# Captura de PDFs (e-books) do portal FIAP — Evidência

> Captura executada em **17/05/2026** via `scripts/fiap_capture_all_phases.py` usando `agent-browser` autenticado como `fiap-on` (vault criptografado).

## Por que e-book em PDF como padrão?

- Todo capítulo do portal FIAP On (sessão Conteúdo do Curso) oferta um **E-Book PDF** com o mesmo conteúdo da aula HTML interativa.
- PDF é a fonte **canônica e completa** da matéria; HTML do leitor depende de iframes e fonte JS dinâmica.
- Baixar PDF é **muito mais rápido** que iterar slides (~1 req por capítulo vs. dezenas de clicks).
- Por isso o orquestrador `fiap_capture_all_phases.py` baixa **apenas PDFs por padrão**. Para conteúdo HTML adicional use `--slides`; para ZIPs de assets use `--assets`.

## Como o download funciona

1. Login persistente via `agent-browser --session-name fiap-on auth login fiap-on`.
2. Para cada **botão FASE** detectado na home (`https://on.fiap.com.br/local/conteudocurso/`):
   - Captura header da fase ativa antes do clique.
   - Clica no botão da fase, dispensa modais (ex.: "Você ganhou uma Flag").
   - Espera o header trocar para `Fase N - <tema>` (poll até 10s).
   - Se não trocar (ou retornar `0` capítulos) → fase marcada como **bloqueada/indisponível**.
3. Para cada capítulo da fase:
   - Abre `/mod/conteudospdf/view.php?id=<N>` (leitor PDF do FIAP).
   - Extrai o `iframe.src` do leitor (`.../leitor/web/index.php?file=<URL_DO_PDF>`).
   - Decodifica e re-encoda o parâmetro `file=` (path com espaços/acentos).
   - Baixa via `curl` usando **cookie jar exportado do agent-browser** (formato Netscape) e `Referer` do viewer (Moodle exige).
4. Dedupe defensivo: se 100% dos capítulos da fase já foram baixados em fase anterior, marca como bloqueada (fallback do portal).

## Resultado da execução

| Fase | Status | Capítulos | Tamanho |
|------|--------|-----------|---------|
| FASE 1 | ✓ liberada | 9 PDFs | 8.3 MB |
| FASE 2 | ✓ liberada | 11 PDFs | 10.7 MB |
| FASE 3 | ✓ liberada (atual: 22/04 → 19/05) | 12 PDFs | 12.0 MB |
| FASE 4 | ⨯ indisponível (ainda não liberada) | 0 | 0 MB |
| **Total** | — | **32 PDFs** | **~32 MB** |

Saída em `docs/validation/captures/fases/` com a árvore:

```
docs/validation/captures/fases/
├── INDEX.json                 # resumo consolidado de todas as fases
├── portal_home.png            # screenshot do dashboard
├── portal_snapshot.txt        # snapshot acessibilidade da home
├── fase1/
│   ├── INDEX.json             # metadados da fase
│   ├── home.png
│   ├── home_snapshot.txt
│   ├── cap01_cap_1_-_play_no_seu_desenvolvimento_como/
│   │   └── 1TIAOA - Fase 1 - Cap01 - Play na sua carreira em IA_RevFinal.pdf
│   ├── cap02_*/...
│   └── cap09_*/...
├── fase2/ (mesma estrutura, 11 caps)
├── fase3/ (mesma estrutura, 12 caps)
└── fase4/ (INDEX.json com bloqueada=true)
```

## Comandos úteis

```bash
# captura padrão (todas as fases liberadas, só PDFs)
python3 scripts/fiap_capture_all_phases.py

# só Fase 3, primeiros 2 capítulos (smoke test rápido)
python3 scripts/fiap_capture_all_phases.py --phases 3 --max-chapters 2

# PDFs + ZIPs de assets
python3 scripts/fiap_capture_all_phases.py --assets

# também captura conteúdo HTML iterando slides (LENTO; só quando explicitamente pedido)
python3 scripts/fiap_capture_all_phases.py --slides

# só HTML, sem PDF
python3 scripts/fiap_capture_all_phases.py --no-pdf --slides

# preserva capturas anteriores em vez de limpar a pasta
python3 scripts/fiap_capture_all_phases.py --keep-output
```

## Detalhes técnicos importantes

### Cookie jar (Netscape)

`agent-browser cookies --json` retorna `{success, data:{cookies:[…]}}`. O script converte para o formato Netscape exigido por `curl -b`, mantendo `MoodleSession`, `jwt`, `sesskey` (cookies de autenticação do Moodle FIAP).

### URL real do PDF

```text
Página do capítulo (view):   https://on.fiap.com.br/mod/conteudospdf/view.php?id=605920
Iframe do leitor:            https://on.fiap.com.br/mod/conteudospdf/leitor/web/index.php?file=<URL_ENCODED>
URL real (param `file`):     https://on.fiap.com.br/pluginfile.php/<resource>/local_conteudospdf/conteudopdf/<id>/<arquivo>.pdf
```

O Moodle **bloqueia** o download direto do `pluginfile.php` sem `Referer` apontando para o `view.php` correspondente (retorna HTML "Sinto muito, o arquivo não foi encontrado"). O script sempre envia o Referer correto.

### Race condition entre cliques de fase

O portal carrega todas as fases no DOM e troca via JS. Para evitar capturar o conteúdo da fase errada após o clique:

1. **Antes** do clique: captura `Fase N - <tema>` ativo no momento.
2. **Depois** do clique: faz poll por até 10s aguardando o header trocar para `Fase <numero clicado>`.
3. Se o header **não** mudar, considera que a fase está indisponível (Moodle volta a exibir a fase ativa como fallback).

### Modais "Você ganhou uma Flag"

Ao clicar em fases concluídas (ex.: Fase 1 já encerrada, ou Fase 4 mostrando flag da Fase 3 atual), o portal abre um modal de premiação que bloqueia o snapshot. O script fecha qualquer modal antes e depois do clique via `document.querySelector('[role=dialog] button').click()`.

## Limitações conhecidas

- Cap 11 das fases 1/2/3 às vezes referencia PDFs com nomes de outras disciplinas (`Cap1 - Mercado e Tecnologia`, `Cap2 - Governanca…`, `Cap3 - Ciencia e Tecnologia`) — é o conteúdo correto, o nome do arquivo no Moodle é genérico.
- Fase 4 só será capturável após sua liberação no portal (estimado pós-19/05/2026).
- Se o `sesskey` rotacionar entre fases, o script re-exporta cookies entre uma fase e outra para evitar 403.
