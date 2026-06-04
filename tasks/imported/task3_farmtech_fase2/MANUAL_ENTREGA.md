# Manual de Entrega — Task 3 (FarmTech Fase 2)

Prazo: **21/04/2026 23h59**.

Este manual é a lista de "coisas que só o Higor pode fazer" para finalizar
a entrega — código e documentação já estão prontos.

---

## 0. Conferência rápida

A pasta `task3_farmtech_fase2/` deve conter:

- [x] `esp32/sketch.ino`, `diagram.json`, `wokwi.toml`, `libraries.txt`
- [x] `opcional1_openweather/clima.py`, `requirements.txt`, `README.md`
- [x] `opcional2_analise/irrigacao_stats.R`, `leituras_exemplo.csv`, `README.md`
- [x] `docs/diagrama_logica.md`
- [x] `README.md`, `MANUAL_ENTREGA.md`
- [ ] `docs/circuito_wokwi.png` — você vai gerar agora (passo 2)
- [ ] `link_video.txt` — você vai preencher depois de gravar (passo 5)

---

## 1. Subir o circuito no Wokwi

1. Abra <https://wokwi.com/> → **New Project** → **ESP32**.
2. Na aba **sketch.ino**, cole o conteúdo de `esp32/sketch.ino`.
3. Na aba **diagram.json**, cole o conteúdo de `esp32/diagram.json`.
4. Menu **Library Manager** → adicione:
   - `DHT sensor library` (Adafruit)
   - `Adafruit Unified Sensor` (puxa automaticamente)
5. ▶ **Start simulation**.
6. Verifique no Serial Monitor se as leituras aparecem a cada 2s.

### Teste rápido
- Clique no DHT22 → umidade ~40% → relé deve **LIGAR** (se pH e NPK estiverem OK).
- Arraste o slider do LDR para pH fora de 5.5–6.5 → relé deve **DESLIGAR**.
- Digite no Serial Monitor: `CHUVA=1` + Enter → relé **DESLIGA** imediatamente.
- Digite `CHUVA=0` + Enter → volta ao normal.

---

## 2. Capturar o circuito

Com a simulação rodando, tire um **print da tela do Wokwi** mostrando o
circuito + Serial Monitor. Salve em:

```
task3_farmtech_fase2/docs/circuito_wokwi.png
```

> Dica: um print com o relé **ligado** (LED vermelho aceso no módulo) fica
> mais visual e demonstra o funcionamento.

---

## 3. (Opcional 1) OpenWeather

Só se quiser demonstrar no vídeo:

```bash
cd task3_farmtech_fase2/opcional1_openweather
pip install -r requirements.txt
# registra em https://openweathermap.org/api e pega a chave gratuita
export OPENWEATHER_API_KEY=sua_chave
python clima.py --cidade "Sao Paulo,BR"
# OU, se não tiver chave, use o modo simulado:
python clima.py --simular-chuva 1
```

Copie a linha `CHUVA=<0|1>` e cole no Serial Monitor do Wokwi.

---

## 4. (Opcional 2) Análise em R

```bash
cd task3_farmtech_fase2/opcional2_analise
Rscript irrigacao_stats.R
```

Saída no console mostra média, desvio padrão, teste t e recomendação. Também
gera `graficos/boxplot_umidade_ph.png`.

---

## 5. Gravar o vídeo (até 5 minutos)

### Roteiro sugerido (~4min)

**(0:00–0:20) Abertura**
- "Olá, sou Higor Henrique Garcia, RM 571820, Squad WOLF. Essa é a Fase 2
  do projeto FarmTech Solutions — sistema de irrigação inteligente para uma
  plantação de café com ESP32."

**(0:20–1:00) Circuito**
- Mostra o Wokwi rodando.
- Aponta cada componente: 3 botões (NPK), LDR (pH), DHT22 (umidade), relé azul.
- "Como no Wokwi não existem sensores agrícolas, usamos substituições:
  botões para NPK, LDR para pH e DHT22 para umidade do solo."

**(1:00–2:30) Demonstração da lógica (café)**
- "A cultura escolhida foi o café — pH ideal 5.5 a 6.5, umidade do solo
  entre 60 e 80%."
- Baixa a umidade no DHT22 → relé LIGA (explica: umidade < 60%, pH ok, NPK ok).
- Move o slider do LDR para fora da faixa → relé DESLIGA (explica: pH ruim).
- Despressiona 2 botões NPK → mesmo com solo seco, relé DESLIGA.

**(2:30–3:30) Opcional 1 — OpenWeather**
- Mostra o terminal rodando `python clima.py --cidade "Sao Paulo,BR"`.
- Explica o `CHUVA=<0|1>` e cola no Serial Monitor.
- "Se houver previsão de chuva, a irrigação é suspensa automaticamente."

**(3:30–4:30) Opcional 2 — R**
- Mostra `Rscript irrigacao_stats.R`.
- Aponta a média, o teste t e a recomendação final.
- Mostra o boxplot gerado.

**(4:30–5:00) Fechamento**
- "Todo o código, diagrama e documentação estão no repositório GitHub
  (link na descrição). Obrigado!"

### Configurações no YouTube
- Visibilidade: **Não listado** (obrigatório pelo enunciado).
- Título sugerido: `FarmTech Fase 2 — Irrigação Inteligente (ESP32 + Café)`.
- Cole o link final em `link_video.txt`.

---

## 6. GitHub

```bash
# Criar repo novo (ex.: farmtech-fase2)
gh repo create farmtech-fase2 --private --source=task3_farmtech_fase2 --push
# OU manual:
#   1. Criar repo no github.com
#   2. cd task3_farmtech_fase2
#   3. git init && git add . && git commit -m "FarmTech Fase 2 — entrega"
#   4. git remote add origin <url>
#   5. git push -u origin main
```

> **Antes de fazer push, me avise no chat** que eu preparo os commits no
> monorepo WOLF. O enunciado pede repositório separado para esta task.

---

## 7. Submissão na FIAP

Enviar o **link do repo GitHub** (com `README.md` renderizado) e garantir
que o vídeo no YouTube esteja **Não listado**.

---

## 8. Checklist final

- [ ] Circuito funciona no Wokwi
- [ ] Print salvo em `docs/circuito_wokwi.png`
- [ ] Vídeo gravado (≤ 5min)
- [ ] Vídeo postado no YouTube como **Não listado**
- [ ] Link em `link_video.txt`
- [ ] Repo GitHub criado e com push
- [ ] Link do repo submetido na FIAP
