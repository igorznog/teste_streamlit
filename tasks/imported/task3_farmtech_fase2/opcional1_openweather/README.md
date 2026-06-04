# Opcional 1 — Integração com OpenWeather

Script `clima.py` consulta a API pública [OpenWeather](https://openweathermap.org/api)
e decide se há chuva prevista nas próximas horas. A saída é o comando
`CHUVA=<0|1>` que o sketch do ESP32 consome via `Serial`.

## Instalação

```bash
pip install -r requirements.txt
```

## Chave da API

1. Registre-se gratuitamente em https://openweathermap.org/api
2. Exporte a chave (ou passe por `--api-key`):

```bash
export OPENWEATHER_API_KEY=sua_chave_aqui
```

## Uso

Apenas consultar e imprimir o comando (você copia no Serial Monitor do Wokwi):

```bash
python clima.py --cidade "Sao Paulo,BR"
```

Enviar direto via porta serial (ESP32 físico ou Wokwi via wokwi-cli):

```bash
python clima.py --cidade "Sao Paulo,BR" --porta /dev/ttyUSB0
```

Simular chuva para ensaio/gravação do vídeo (não chama a API):

```bash
python clima.py --simular-chuva 1
```

## Parâmetros

| Flag | Default | Descrição |
|------|---------|-----------|
| `--cidade` | `Sao Paulo,BR` | Cidade no formato `Nome,PaisISO` |
| `--api-key` | env `OPENWEATHER_API_KEY` | Chave da API OpenWeather |
| `--horas` | 6 | Horizonte de análise em horas |
| `--limiar-pop` | 0.4 | Probabilidade mínima (0..1) para considerar chuva |
| `--porta` | — | Porta serial opcional |
| `--simular-chuva` | — | `0` ou `1` — pula a API e força o valor |

## Regra de decisão

Pega as próximas `horas/3` janelas do endpoint *5-day / 3-hour forecast*. Se
qualquer janela tiver `pop >= limiar` **ou** `rain.3h > 0.1 mm`, emite
`CHUVA=1`. Caso contrário, `CHUVA=0`.
