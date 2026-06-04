#!/usr/bin/env python3
"""Sobe o Streamlit em background e captura screenshots com Playwright.

Requisitos:
    pip install playwright streamlit pandas plotly
    playwright install chromium

Uso:
    python3 scripts/capture_dashboard_prints.py
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DASHBOARD = ROOT / "dashboard"
PRINTS = ROOT / "prints"
URL = "http://127.0.0.1:8501"
STARTUP_WAIT_S = 25


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Instale: pip install playwright && playwright install chromium", file=sys.stderr)
        return 1

    PRINTS.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "true",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false",
        ],
        cwd=DASHBOARD,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(f"[•] Streamlit PID {proc.pid} — aguardando {STARTUP_WAIT_S}s ...", flush=True)
    time.sleep(STARTUP_WAIT_S)

    shots = [
        ("dash_01_home", URL, False),
        ("dash_02_umidade_ph", URL, False),
        ("dash_03_npk", URL, False),
        ("dash_04_bomba_por_hora", URL, False),
        ("dash_05_chuva_prevista", URL, True),
    ]

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            page.goto(URL, wait_until="networkidle", timeout=120_000)
            page.wait_for_timeout(3000)

            dest = PRINTS / "dash_01_home.png"
            page.screenshot(path=str(dest), full_page=True)
            print(f"    ✓ {dest.name}", flush=True)

            # Aba Umidade & pH (geralmente já visível)
            tabs = page.get_by_role("tab")
            if tabs.count() >= 2:
                tabs.nth(0).click()
                page.wait_for_timeout(1500)
            page.screenshot(path=str(PRINTS / "dash_02_umidade_ph.png"), full_page=True)
            print("    ✓ dash_02_umidade_ph.png", flush=True)

            if tabs.count() >= 2:
                tabs.nth(1).click()
                page.wait_for_timeout(1500)
            page.screenshot(path=str(PRINTS / "dash_03_npk.png"), full_page=True)
            print("    ✓ dash_03_npk.png", flush=True)

            if tabs.count() >= 3:
                tabs.nth(2).click()
                page.wait_for_timeout(1500)
            page.screenshot(path=str(PRINTS / "dash_04_bomba_por_hora.png"), full_page=True)
            print("    ✓ dash_04_bomba_por_hora.png", flush=True)

            # Marcar chuva prevista na sidebar
            chuva = page.get_by_text("Chuva prevista", exact=False)
            if chuva.count():
                label = page.locator("label").filter(has_text="Chuva")
                if label.count():
                    label.first.click()
                    page.wait_for_timeout(1000)
            page.screenshot(path=str(PRINTS / "dash_05_chuva_prevista.png"), full_page=True)
            print("    ✓ dash_05_chuva_prevista.png", flush=True)

            browser.close()
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()

    print(f"\n✓ Screenshots em {PRINTS}/", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
