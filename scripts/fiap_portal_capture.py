#!/usr/bin/env python3
"""Automação de captura do portal FIAP On (https://on.fiap.com.br).

Estratégia: navegador Chromium controlado por Playwright com perfil persistente
(em ~/.cache/fiap-portal-capture). O aluno faz login uma vez (incluindo MFA);
nas próximas execuções a sessão é reaproveitada.

Comandos:
    login                              Abre janela para login manual; salva sessão.
    capture <url>                      Captura HTML, screenshot full-page, texto e
                                       lista de links/imagens em uma URL específica.
    capture-task <url>                 Igual a capture, porém também preenche o
                                       template de captura em docs/templates.
    status                             Mostra onde a sessão está salva.

Saídas (default em docs/validation/captures/):
    <slug>_<timestamp>.html            HTML completo da página renderizada.
    <slug>_<timestamp>.png             Screenshot full-page.
    <slug>_<timestamp>.txt             Texto visível (innerText do body).
    <slug>_<timestamp>.json            Metadados, links e imagens estruturados.

Regras de segurança:
    - NUNCA aceita senha como argumento; o login acontece no navegador.
    - O diretório de perfil é local da máquina e NÃO entra no Git.
    - Falhou? Faz fallback orientando o template manual.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Erro: dependência 'playwright' não encontrada.", file=sys.stderr)
    print("Instale com:", file=sys.stderr)
    print("  pip install -r scripts/requirements-fiap-capture.txt", file=sys.stderr)
    print("  python3 -m playwright install chromium", file=sys.stderr)
    sys.exit(2)


PORTAL_URL = "https://on.fiap.com.br"
DEFAULT_PROFILE = Path.home() / ".cache" / "fiap-portal-capture" / "profile"
DEFAULT_OUT = Path("docs/validation/captures")


def _now_slug() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _ensure_profile_dir() -> Path:
    DEFAULT_PROFILE.mkdir(parents=True, exist_ok=True)
    return DEFAULT_PROFILE


def cmd_status(_: argparse.Namespace) -> int:
    profile = _ensure_profile_dir()
    exists = any(profile.iterdir())
    print(f"Perfil de sessão: {profile}")
    print("Status: ativa (login provavelmente já feito)" if exists else "Status: vazia (rodar `login` primeiro)")
    return 0


def cmd_login(args: argparse.Namespace) -> int:
    profile = _ensure_profile_dir()
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(profile),
            headless=False,
            viewport={"width": args.width, "height": args.height},
            locale="pt-BR",
        )
        page = context.new_page()
        page.goto(PORTAL_URL, wait_until="domcontentloaded")
        print("Janela aberta. Faça login no portal (incluindo MFA, se houver).")
        print("Quando estiver no dashboard autenticado, volte aqui e pressione ENTER.")
        try:
            input()
        except (KeyboardInterrupt, EOFError):
            print("\nLogin interrompido. Sessão pode estar incompleta.")
        context.close()
    print(f"Sessão salva em: {profile}")
    return 0


def _capture_page(page, url: str, wait_extra_ms: int) -> dict:
    page.goto(url, wait_until="networkidle")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(wait_extra_ms)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)

    title = page.title()
    html = page.content()
    text = page.evaluate("() => document.body.innerText")
    images = page.evaluate(
        """() => Array.from(document.images).map(img => ({
            src: img.src,
            alt: img.alt || '',
            width: img.naturalWidth,
            height: img.naturalHeight
        }))"""
    )
    links = page.evaluate(
        """() => Array.from(document.querySelectorAll('a[href]'))
            .map(a => ({ href: a.href, text: (a.innerText || '').trim() }))
            .filter(l => l.text || l.href)"""
    )
    return {
        "title": title,
        "html": html,
        "text": text,
        "images": images,
        "links": links,
    }


def cmd_capture(args: argparse.Namespace) -> int:
    profile = _ensure_profile_dir()
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    slug = args.slug or "capture"
    base = out_dir / f"{slug}_{_now_slug()}"

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(profile),
            headless=args.headless,
            viewport={"width": args.width, "height": args.height},
            locale="pt-BR",
        )
        page = context.new_page()
        try:
            data = _capture_page(page, args.url, args.wait_ms)
        except Exception as exc:
            context.close()
            print(f"Erro ao capturar {args.url}: {exc}", file=sys.stderr)
            print("Se o portal exigir login, rode primeiro: fiap_portal_capture.py login", file=sys.stderr)
            return 3

        html_path = base.with_suffix(".html")
        png_path = base.with_suffix(".png")
        txt_path = base.with_suffix(".txt")
        json_path = base.with_suffix(".json")

        html_path.write_text(data["html"], encoding="utf-8")
        page.screenshot(path=str(png_path), full_page=True)
        txt_path.write_text(data["text"], encoding="utf-8")

        meta = {
            "url": args.url,
            "title": data["title"],
            "captured_at": datetime.now().isoformat(timespec="seconds"),
            "files": {
                "html": html_path.name,
                "screenshot": png_path.name,
                "text": txt_path.name,
            },
            "images": data["images"],
            "links": data["links"],
        }
        json_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        context.close()

    print(f"Captura concluída em: {base}.*")
    print(f"  HTML:        {html_path}")
    print(f"  Screenshot:  {png_path}")
    print(f"  Texto:       {txt_path}")
    print(f"  Metadados:   {json_path}")
    return 0


def cmd_capture_task(args: argparse.Namespace) -> int:
    rc = cmd_capture(args)
    if rc != 0:
        return rc
    template_path = Path("docs/templates/FIAP_TASK_CAPTURE_TEMPLATE.md")
    if not template_path.exists():
        print(f"Aviso: template não encontrado em {template_path}.", file=sys.stderr)
        return 0
    print("\nPróximo passo sugerido:")
    print(f"  1. Abra {template_path} e cole o conteúdo do .txt gerado.")
    print("  2. Rode: python3 scripts/parse_fiap_task_capture.py <template_preenchido>")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fiap_portal_capture.py",
        description="Captura automática de páginas do portal FIAP On com sessão persistente.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_status = sub.add_parser("status", help="Mostra onde a sessão está salva.")
    p_status.set_defaults(func=cmd_status)

    p_login = sub.add_parser("login", help="Abre navegador para login manual e salva a sessão.")
    p_login.add_argument("--width", type=int, default=1366)
    p_login.add_argument("--height", type=int, default=900)
    p_login.set_defaults(func=cmd_login)

    def add_capture_args(p: argparse.ArgumentParser) -> None:
        p.add_argument("url", help="URL absoluta da página a capturar.")
        p.add_argument("--out-dir", default=str(DEFAULT_OUT), help=f"Diretório de saída (default: {DEFAULT_OUT}).")
        p.add_argument("--slug", default=None, help="Nome curto para os arquivos.")
        p.add_argument("--headless", action="store_true", help="Roda sem janela visível.")
        p.add_argument("--width", type=int, default=1366)
        p.add_argument("--height", type=int, default=900)
        p.add_argument("--wait-ms", type=int, default=1500, help="Tempo extra de espera após scroll para lazy load.")

    p_cap = sub.add_parser("capture", help="Captura uma página (precisa de login prévio).")
    add_capture_args(p_cap)
    p_cap.set_defaults(func=cmd_capture)

    p_task = sub.add_parser("capture-task", help="Captura uma página e orienta preencher o template de task.")
    add_capture_args(p_task)
    p_task.set_defaults(func=cmd_capture_task)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args) or 0)


if __name__ == "__main__":
    raise SystemExit(main())
