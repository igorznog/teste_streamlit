"""FarmTech Solutions — Fase 2 — Opcional 1

Consulta a API OpenWeather (5-day / 3-hour forecast) e decide se há
previsão de chuva nas próximas horas. Emite o comando que o ESP32
consome via Serial:

    CHUVA=1  -> há chuva prevista, irrigação deve ser suspensa
    CHUVA=0  -> sem chuva prevista

Uso:
    python clima.py --cidade "Sao Paulo,BR" --api-key SUA_CHAVE
    python clima.py --cidade "Sao Paulo,BR" --api-key SUA_CHAVE \
                    --porta /dev/ttyUSB0   # envia automaticamente

Sem --porta, o script apenas imprime o comando CHUVA=<0|1> para que o
Higor copie e cole no Serial Monitor do Wokwi.

Autor: Squad WOLF
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from dataclasses import dataclass
from typing import Optional

API_URL = "https://api.openweathermap.org/data/2.5/forecast"
DEFAULT_HORAS = 6
DEFAULT_LIMIAR_POP = 0.4  # probabilidade de precipitação >= 40% -> considera chuva


@dataclass
class Previsao:
    momento: str
    pop: float  # 0.0 a 1.0
    chuva_mm: float
    descricao: str


def consultar_openweather(cidade: str, api_key: str) -> list[Previsao]:
    import requests  # import tardio: permite --simular-chuva sem a dependência

    params = {
        "q": cidade,
        "appid": api_key,
        "units": "metric",
        "lang": "pt_br",
    }
    resp = requests.get(API_URL, params=params, timeout=15)
    resp.raise_for_status()
    dados = resp.json()

    lista: list[Previsao] = []
    for item in dados.get("list", []):
        chuva_mm = 0.0
        if isinstance(item.get("rain"), dict):
            chuva_mm = float(item["rain"].get("3h", 0.0))
        descricao = item["weather"][0]["description"] if item.get("weather") else ""
        lista.append(
            Previsao(
                momento=item.get("dt_txt", "?"),
                pop=float(item.get("pop", 0.0)),
                chuva_mm=chuva_mm,
                descricao=descricao,
            )
        )
    return lista


def decidir_chuva(
    previsoes: list[Previsao],
    horas: int = DEFAULT_HORAS,
    limiar_pop: float = DEFAULT_LIMIAR_POP,
) -> tuple[bool, list[Previsao]]:
    # OpenWeather entrega 1 amostra a cada 3h; pegamos as primeiras N.
    janelas = max(1, horas // 3)
    proximas = previsoes[:janelas]
    chuva = any(p.pop >= limiar_pop or p.chuva_mm > 0.1 for p in proximas)
    return chuva, proximas


def enviar_via_serial(porta: str, comando: str) -> None:
    try:
        import serial  # type: ignore
    except ImportError:
        print(
            "[aviso] pyserial não instalado. Instale com 'pip install pyserial' "
            "ou copie o comando manualmente no Serial Monitor.",
            file=sys.stderr,
        )
        return

    try:
        with serial.Serial(porta, baudrate=115200, timeout=2) as s:
            time.sleep(2)  # aguarda ESP32 subir
            s.write((comando + "\n").encode("utf-8"))
            s.flush()
            print(f"[ok] Comando '{comando}' enviado para {porta}")
    except Exception as exc:
        print(f"[erro] Falha ao enviar via serial: {exc}", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Consulta OpenWeather e emite CHUVA=<0|1>")
    ap.add_argument("--cidade", default="Sao Paulo,BR",
                    help="Cidade no formato 'Nome,PaisISO' (default: Sao Paulo,BR)")
    ap.add_argument("--api-key", default=os.environ.get("OPENWEATHER_API_KEY", ""),
                    help="Chave da API OpenWeather (ou variável OPENWEATHER_API_KEY)")
    ap.add_argument("--horas", type=int, default=DEFAULT_HORAS,
                    help=f"Horizonte de análise em horas (default: {DEFAULT_HORAS})")
    ap.add_argument("--limiar-pop", type=float, default=DEFAULT_LIMIAR_POP,
                    help="Probabilidade mínima para considerar chuva (0..1)")
    ap.add_argument("--porta", default=None,
                    help="Porta serial opcional (ex.: /dev/ttyUSB0 ou COM3)")
    ap.add_argument("--simular-chuva", choices=["0", "1"], default=None,
                    help="Pula a API e força o valor (útil para gravar o vídeo)")
    return ap.parse_args()


def main() -> int:
    args = parse_args()

    if args.simular_chuva is not None:
        chuva = args.simular_chuva == "1"
        comando = f"CHUVA={1 if chuva else 0}"
        print(f"[modo simulado] {comando}")
        if args.porta:
            enviar_via_serial(args.porta, comando)
        return 0

    if not args.api_key:
        print(
            "[erro] forneça --api-key ou defina OPENWEATHER_API_KEY.\n"
            "       Registre-se grátis em https://openweathermap.org/api",
            file=sys.stderr,
        )
        return 2

    try:
        previsoes = consultar_openweather(args.cidade, args.api_key)
    except ImportError:
        print("[erro] Biblioteca 'requests' não instalada. "
              "Rode: pip install -r requirements.txt", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"[erro] Falha na consulta à API: {exc}", file=sys.stderr)
        return 1

    chuva, janelas = decidir_chuva(previsoes, args.horas, args.limiar_pop)

    print(f"Cidade: {args.cidade}")
    print(f"Horizonte analisado: próximas {args.horas}h "
          f"({len(janelas)} janela(s) de 3h)")
    for p in janelas:
        print(f"  {p.momento} | POP={p.pop*100:5.1f}% | "
              f"chuva={p.chuva_mm:.2f}mm | {p.descricao}")

    comando = f"CHUVA={1 if chuva else 0}"
    print(f"\n>>> {comando}")

    if args.porta:
        enviar_via_serial(args.porta, comando)
    else:
        print("(copie a linha acima no Serial Monitor do Wokwi)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
