# FarmTech Solutions — Fase 2

## Sistema de Irrigação Inteligente com ESP32 (cultura: Café)

Squad **WOLF** — Projeto PBL (Fase 2) da FIAP.

Este projeto evolui o sistema FarmTech (Fase 1) adicionando um dispositivo
IoT simulado no [Wokwi.com](https://wokwi.com/) que monitora os nutrientes
**N-P-K**, o **pH** e a **umidade do solo** de uma plantação de **café**
(*Coffea arabica*) e liga/desliga automaticamente uma **bomba d'água**
(relé azul) conforme a necessidade real da cultura.

---

## 1. Componentes simulados

No Wokwi não existem sensores agrícolas — por isso adotamos as seguintes
substituições didáticas propostas pelo enunciado:

| Sensor real | Substituto no Wokwi | Pino ESP32 | Função |
|-------------|---------------------|------------|--------|
| Nível de Nitrogênio (N) | Chave slide (interruptor) | **GPIO 4** (INPUT_PULLUP) | `true` se N presente |
| Nível de Fósforo (P)    | Chave slide (interruptor) | **GPIO 5** (INPUT_PULLUP) | `true` se P presente |
| Nível de Potássio (K)   | Chave slide (interruptor) | **GPIO 18** (INPUT_PULLUP) | `true` se K presente |
| pH do solo              | LDR (photoresistor) | **GPIO 34** (ADC) | valor analógico 0–4095 → pH 0–14 |
| Umidade do solo         | DHT22 | **GPIO 15** | umidade (%) e temperatura (°C) |
| Bomba d'água            | Módulo de relé azul | **GPIO 23** (OUTPUT) | liga/desliga a bomba |
| LED informativo         | LED onboard | **GPIO 2** | pisca a cada leitura |

> **Reforço do enunciado**: como não temos sensor de pH, o aluno **altera
> manualmente o slider do LDR** no Wokwi sempre que mexe nos switches NPK —
> isso simula o efeito dos nutrientes sobre o pH do solo.
>
> **Nota**: o enunciado pede "botões verdes" como substituto dos níveis de
> N, P e K (true/false). Usamos **chaves slide** (slide switches) em vez de
> pushbuttons momentâneos porque representam melhor uma "presença constante
> de nutriente": clicou → trava em ligado; clicou de novo → desliga. Evita
> ter que segurar o mouse em 3 botões ao mesmo tempo durante a demonstração.

---

## 2. Circuito no Wokwi

O diagrama está em [`esp32/diagram.json`](esp32/diagram.json) (abrir no Wokwi).

![Circuito FarmTech Fase 2](docs/circuito_wokwi.png)

> **Pendência**: capturar o print do circuito em execução e salvar como
> `docs/circuito_wokwi.png`.

---

## 3. Lógica de decisão da bomba

Implementada em [`esp32/sketch.ino`](esp32/sketch.ino) na função
`decidir_irrigacao(...)`. O fluxograma e a tabela verdade completos estão
em [`docs/diagrama_logica.md`](docs/diagrama_logica.md).

### Regras (cultura: Café)

1. **Chuva prevista** (recebida via Serial no formato `CHUVA=1`) → bomba
   desligada.
2. **Umidade ≥ 80%** → bomba desligada (solo encharcado).
3. **Umidade < 60%** → liga a bomba **se** `pH ∈ [5.0, 7.0]` **e** pelo menos
   2 dos 3 botões NPK estiverem pressionados.
4. **60% ≤ Umidade < 70%** → irrigação preventiva apenas se **todos** os
   nutrientes estiverem presentes e pH dentro da faixa.
5. Demais casos → bomba desligada.

> **Nota sobre a faixa de pH**: o ideal do café é 5.5–6.5. Como o enunciado
> permite ampliar a escala para melhorar a manipulação do slider do LDR no
> Wokwi, adotamos **5.0–7.0** (tolerância de ±0.5) — mantém realismo
> agronômico e garante que o aluno consiga acertar a faixa no slider.

### Por que café?

| Parâmetro | Faixa ideal | Fonte |
|-----------|-------------|-------|
| pH do solo | 5.5 – 6.5 | Embrapa Café |
| Umidade do solo | 60–80% | Boletins MAPA |
| Nutrientes chave | N + K altos, P moderado | Manual de cafeicultura |

Irrigar fora dessas faixas desperdiça água e pode até prejudicar a planta
(encharcamento → doenças radiculares; pH ácido demais → toxicidade por
alumínio; pH alcalino → bloqueio de micronutrientes).

> 📚 Justificativa completa, referências bibliográficas e o raciocínio por
> trás de **cada regra** da lógica estão em
> [`docs/fundamentacao_agronomica.md`](docs/fundamentacao_agronomica.md).

---

## 4. Como rodar no Wokwi

1. Entre em <https://wokwi.com/> e crie um projeto **ESP32**.
2. Cole o conteúdo de `esp32/sketch.ino` na aba **sketch.ino**.
3. Cole o conteúdo de `esp32/diagram.json` na aba **diagram.json**.
4. Adicione a biblioteca **DHT sensor library** (by Adafruit) em
   *Library Manager* — vai puxar automaticamente o *Adafruit Unified
   Sensor*. Ou use o arquivo `esp32/libraries.txt`.
5. Clique em ▶ **Start**.
6. Interaja:
   - Aperte os botões verdes para alterar N, P, K.
   - Ajuste o slider do LDR (manualmente) para simular pH.
   - Clique no DHT22 para mudar umidade e temperatura.
   - Digite `CHUVA=1` ou `CHUVA=0` no Serial Monitor para simular chuva.

O ciclo de leitura roda a cada **2 segundos**, com log completo no
Serial Monitor.

---

## 5. Ir Além — Opcional 1 (Python + OpenWeather)

O script [`opcional1_openweather/clima.py`](opcional1_openweather/clima.py)
consulta a API pública OpenWeather e emite o comando `CHUVA=<0|1>` que o
ESP32 consome via Serial. Se houver previsão de chuva (POP ≥ 40% ou
precipitação > 0.1mm nas próximas 6h), a irrigação é suspensa.

```bash
cd opcional1_openweather
pip install -r requirements.txt
export OPENWEATHER_API_KEY=sua_chave
python clima.py --cidade "Sao Paulo,BR"
# depois copie a linha CHUVA=<0|1> para o Serial Monitor do Wokwi
```

Modos de operação:

- **Consulta + print** (padrão): imprime o comando para o aluno copiar.
- **Consulta + envio serial**: `--porta /dev/ttyUSB0` — envia direto para
  a porta serial (funciona com ESP32 físico ou Wokwi com `wokwi-cli`).
- **Simulado**: `--simular-chuva 1` — pula a API (útil pra gravar o vídeo).

Detalhes em [`opcional1_openweather/README.md`](opcional1_openweather/README.md).

---

## 6. Ir Além — Opcional 2 (Análise estatística em R)

O script [`opcional2_analise/irrigacao_stats.R`](opcional2_analise/irrigacao_stats.R)
lê um CSV com leituras históricas dos sensores e recomenda ligar ou desligar
a bomba com base em:

1. Estatísticas descritivas (média e desvio padrão de pH e umidade).
2. **Teste t unilateral** comparando a umidade média com o alvo do café
   (70%): `H0: média >= 70%`.
3. Decisão final: liga a bomba se `p-valor < 0.05` e pH médio estiver na
   faixa ideal.

```bash
cd opcional2_analise
Rscript irrigacao_stats.R
```

Usa apenas **R base** (sem dependências externas). Saída: log no console +
`graficos/boxplot_umidade_ph.png` com as faixas ideais marcadas.

Detalhes em [`opcional2_analise/README.md`](opcional2_analise/README.md).

---

## 7. Estrutura do repositório

```
task3_farmtech_fase2/
├── esp32/
│   ├── sketch.ino          # código C/C++ do ESP32
│   ├── diagram.json        # circuito Wokwi
│   ├── wokwi.toml
│   └── libraries.txt       # libs Arduino usadas
├── opcional1_openweather/
│   ├── clima.py            # Python + OpenWeather
│   ├── requirements.txt
│   └── README.md
├── opcional2_analise/
│   ├── irrigacao_stats.R   # análise estatística em R
│   ├── leituras_exemplo.csv
│   └── README.md
├── docs/
│   ├── circuito_wokwi.png  # print do circuito (gerar no Wokwi)
│   └── diagrama_logica.md  # fluxograma + tabela verdade
├── link_video.txt          # URL do vídeo YouTube (não listado)
├── MANUAL_ENTREGA.md       # roteiro do vídeo + passo-a-passo
└── README.md               # este arquivo
```

---

## 8. Vídeo demonstrativo

Link do YouTube (não listado, até 5min): ver [`link_video.txt`](link_video.txt).

Roteiro completo em [`MANUAL_ENTREGA.md`](MANUAL_ENTREGA.md).

---

## 9. Squad WOLF

Projeto executado como squad solo usando agentes de IA no Cursor (modelo
Arquiteto + subagents executores). O framework WOLF está descrito no
`.cursorrules` da raiz do monorepo e no `TASK_REGISTRY.md`.
