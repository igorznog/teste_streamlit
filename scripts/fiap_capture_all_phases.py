#!/usr/bin/env python3
"""Captura todo o conteúdo de todas as fases visíveis no portal FIAP On.

Por padrão baixa apenas os e-books PDF de cada capítulo (rápido e canônico).
Use `--slides` para também capturar o conteúdo HTML slide-a-slide.
Use `--assets` para também baixar ZIPs de assets quando disponíveis.

Pré-requisitos:
    - agent-browser instalado e Chrome baixado.
    - Credencial salva no vault como `fiap-on`.
    - AGENT_BROWSER_ENCRYPTION_KEY exportada (o script tenta carregar do arquivo).

Fluxo:
    1. `agent-browser --session-name fiap-on auth login fiap-on`
    2. Abre página principal de Conteúdo do curso.
    3. Para cada FASE detectada (FASE 1..FASE N):
        a. Clica no botão da fase.
        b. Captura snapshot + screenshot da home da fase.
        c. Para cada capítulo:
            - Modo PDF (default): baixa o e-book via cookies + Referer.
            - --slides: também captura HTML iterando slides.
            - --assets: também baixa ZIP de assets se houver.
    4. Salva tudo em docs/validation/captures/fases/.
    5. Gera INDEX.json consolidado.

Limita escopo com `--phases 1,3` (CSV) e `--max-chapters N`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "docs" / "validation" / "captures" / "fases"
PORTAL_URL = "https://on.fiap.com.br/local/conteudocurso/"
KEY_FILE = Path.home() / ".agent-browser" / ".encryption-key"
SESSION_NAME = "fiap-on"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148 Safari/537.36"


# ---------- agent-browser wrapper ----------
class AgentBrowserError(RuntimeError):
    pass


def _ensure_key() -> None:
    if "AGENT_BROWSER_ENCRYPTION_KEY" not in os.environ and KEY_FILE.exists():
        os.environ["AGENT_BROWSER_ENCRYPTION_KEY"] = KEY_FILE.read_text().strip()
    os.environ.setdefault("AGENT_BROWSER_ALLOWED_DOMAINS", "on.fiap.com.br,*.fiap.com.br")


def ab(*args: str, timeout: int = 60, check: bool = True) -> str:
    result = subprocess.run(
        ["agent-browser", "--session-name", SESSION_NAME, *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=ROOT,
    )
    if check and result.returncode != 0:
        raise AgentBrowserError(f"agent-browser {' '.join(args)} falhou:\n{result.stderr}")
    return result.stdout


def login() -> None:
    print("[•] Login...", flush=True)
    ab("auth", "login", "fiap-on", timeout=90)


def goto(url: str) -> None:
    ab("open", url, timeout=60)
    ab("wait", "--load", "networkidle", timeout=60, check=False)


def page_title() -> str:
    return ab("get", "title", timeout=15).strip()


def page_url() -> str:
    return ab("get", "url", timeout=15).strip()


def snapshot(interactive: bool = True, urls: bool = True) -> str:
    args = ["snapshot"]
    if interactive:
        args.append("-i")
    if urls:
        args.append("--urls")
    return ab(*args, timeout=45)


def screenshot(path: Path, full: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    args = ["screenshot"]
    if full:
        args.append("--full")
    args.append(str(path))
    ab(*args, timeout=90)


def click(ref: str) -> None:
    ab("click", ref, timeout=30)


def eval_js(js: str) -> str:
    """Roda JS via stdin (evita problemas de shell quoting)."""
    result = subprocess.run(
        ["agent-browser", "--session-name", SESSION_NAME, "eval", "--stdin"],
        input=js, capture_output=True, text=True, timeout=45,
    )
    if result.returncode != 0:
        raise AgentBrowserError(f"eval falhou:\n{result.stderr}")
    return result.stdout


def get_cookies_netscape() -> str:
    """Exporta cookies do agent-browser em formato Netscape (cookie jar)."""
    result = subprocess.run(
        ["agent-browser", "--session-name", SESSION_NAME, "cookies", "--json"],
        capture_output=True, text=True, timeout=15,
    )
    if result.returncode != 0:
        raise AgentBrowserError(f"cookies falhou:\n{result.stderr}")
    raw = json.loads(result.stdout)
    cookies = raw["data"]["cookies"]
    lines = ["# Netscape HTTP Cookie File"]
    for c in cookies:
        domain = c.get("domain", "")
        flag = "TRUE" if domain.startswith(".") else "FALSE"
        path = c.get("path", "/")
        secure = "TRUE" if c.get("secure") else "FALSE"
        exp = int(c.get("expires", 0)) if c.get("expires", 0) > 0 else 0
        prefix = "#HttpOnly_" if c.get("httpOnly") else ""
        lines.append(f"{prefix}{domain}\t{flag}\t{path}\t{secure}\t{exp}\t{c['name']}\t{c['value']}")
    return "\n".join(lines) + "\n"


def close_all() -> None:
    subprocess.run(
        ["agent-browser", "--session-name", SESSION_NAME, "close", "--all"],
        capture_output=True, text=True, timeout=15,
    )


# ---------- regex auxiliares ----------
PHASE_BUTTON_RE = re.compile(r'^- button "(FASE \d+)" \[ref=(e\d+)\]', re.MULTILINE)
CHAPTER_LINK_RE = re.compile(
    r'^- link "Acessar conteúdo (?:do conteúdo )?(.+?)" \[ref=(e\d+), url=([^\]]+)\]',
    re.MULTILINE,
)
EBOOK_LINK_RE = re.compile(
    r'^- link "Acessar E-Book do conteúdo (.+?)" \[ref=(e\d+), url=([^\]]+)\]',
    re.MULTILINE,
)
ASSETS_LINK_RE = re.compile(
    r'^- link "Acessar assets do conteúdo (.+?)" \[ref=(e\d+), url=([^\]]+)\]',
    re.MULTILINE,
)
EXT_LINK_RE = re.compile(r'^- link "ACESSAR" \[ref=(e\d+), url=([^\]]+)\]', re.MULTILINE)
ASSIGNMENT_LINK_RE = re.compile(
    r'^\s+- link "(ENTREGAR|VISUALIZAR)" \[ref=(e\d+), url=([^\]]+)\]', re.MULTILINE,
)

SNAPSHOT_HEADING_RE = re.compile(r'^(\s*)- heading "([^"]+)" \[level=(\d+)', re.MULTILINE)
SNAPSHOT_STATIC_RE = re.compile(r'^(\s*)- StaticText "([^"]+)"', re.MULTILINE)
SLIDE_INDEX_RE = re.compile(r'"(\d+) DE (\d+)"')
NEXT_SLIDE_RE = re.compile(
    r'- button "Próximo slide"(?: \[(?P<state>[^\]]+)\])? \[ref=(?P<ref>e\d+)\]'
)
IFRAME_LINE_RE = re.compile(r'- Iframe(?: "([^"]+)")? \[ref=(e\d+)\]')


@dataclass
class ChapterInfo:
    titulo: str
    url_conteudo: Optional[str] = None
    url_ebook: Optional[str] = None
    url_assets: Optional[str] = None
    pdf_file: Optional[str] = None
    pdf_size_bytes: Optional[int] = None
    assets_file: Optional[str] = None
    slides_dir: Optional[str] = None
    captured_at: Optional[str] = None
    erros: list[str] = field(default_factory=list)


@dataclass
class PhaseInfo:
    nome: str
    url: str
    titulo_pagina: Optional[str] = None
    capitulos: list[ChapterInfo] = field(default_factory=list)
    links_extras: list[str] = field(default_factory=list)
    entregas: list[dict] = field(default_factory=list)
    captured_at: Optional[str] = None
    bloqueada: bool = False
    observacao: Optional[str] = None


# ---------- parsers ----------
def parse_phase_snapshot(snap: str) -> tuple[list[ChapterInfo], list[str], list[dict]]:
    chapters: dict[str, ChapterInfo] = {}
    for titulo, _, url in CHAPTER_LINK_RE.findall(snap):
        chapters.setdefault(titulo, ChapterInfo(titulo=titulo)).url_conteudo = url
    for titulo, _, url in EBOOK_LINK_RE.findall(snap):
        chapters.setdefault(titulo, ChapterInfo(titulo=titulo)).url_ebook = url
    for titulo, _, url in ASSETS_LINK_RE.findall(snap):
        chapters.setdefault(titulo, ChapterInfo(titulo=titulo)).url_assets = url
    extras = [url for _, url in EXT_LINK_RE.findall(snap)]
    entregas = [
        {"acao": label, "url": url}
        for label, _, url in ASSIGNMENT_LINK_RE.findall(snap)
    ]
    return list(chapters.values()), extras, entregas


def slugify(name: str, fallback: str = "item") -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "_", name.strip())
    s = re.sub(r"_+", "_", s).strip("_")
    return s.lower() or fallback


def snapshot_to_markdown(snap: str) -> str:
    lines: list[str] = []
    seen_static_after_heading: set[str] = set()
    pending_static: list[str] = []

    def flush_paragraph() -> None:
        if pending_static:
            paragraph = " ".join(pending_static).strip()
            if paragraph and (not lines or lines[-1] != paragraph):
                lines.append(paragraph)
                lines.append("")
            pending_static.clear()

    for raw in snap.splitlines():
        m_h = SNAPSHOT_HEADING_RE.match(raw)
        if m_h:
            flush_paragraph()
            level = max(1, min(int(m_h.group(3)), 6))
            text = m_h.group(2).strip()
            lines.append(f"{'#' * level} {text}")
            lines.append("")
            seen_static_after_heading.add(text)
            continue
        m_s = SNAPSHOT_STATIC_RE.match(raw)
        if m_s:
            text = m_s.group(2).strip()
            if text in seen_static_after_heading:
                seen_static_after_heading.discard(text)
                continue
            if text:
                pending_static.append(text)
            continue
        m_if = IFRAME_LINE_RE.search(raw)
        if m_if:
            flush_paragraph()
            name = (m_if.group(1) or "iframe sem título").strip()
            lines.append(f"> [iframe embutido] {name}")
            lines.append("")
            continue
    flush_paragraph()
    return "\n".join(lines).rstrip() + "\n"


def collect_iframes(snap: str) -> list[str]:
    return [m.group(1) or "iframe sem título" for m in IFRAME_LINE_RE.finditer(snap)]


# ---------- download de arquivos ----------
def http_download(url: str, dest: Path, cookie_jar: Path, referer: str) -> int:
    """Baixa um arquivo grande via curl com cookies + Referer; retorna bytes."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "curl", "-sSL",
        "-b", str(cookie_jar),
        "-A", USER_AGENT,
        "-H", f"Referer: {referer}",
        "-H", "Accept: application/pdf,application/zip,application/octet-stream,*/*",
        "-o", str(dest),
        "-w", "%{http_code}",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if result.returncode != 0:
        raise RuntimeError(f"curl falhou ({result.returncode}): {result.stderr}")
    status = result.stdout.strip()
    if status and not status.startswith("2"):
        raise RuntimeError(f"HTTP {status} ao baixar {url}")
    return dest.stat().st_size if dest.exists() else 0


def extract_pdf_url_from_viewer(viewer_url: str) -> Optional[str]:
    """Abre a página /mod/conteudospdf/view.php?id=N e extrai o URL real do PDF.

    O leitor PDF do FIAP carrega o arquivo num iframe cujo src tem o formato:
        .../leitor/web/index.php?file=<URL_DO_PDF>
    """
    goto(viewer_url)
    time.sleep(1.0)
    js = (
        "JSON.stringify(Array.from(document.querySelectorAll('iframe'))"
        ".map(f => f.src).filter(s => s && s.includes('leitor')))"
    )
    out = eval_js(js).strip()
    if not out:
        return None
    # output vem como '"["url1","url2"]"' (JSON quoted)
    try:
        # primeiro parse retira o quoting externo do agent-browser
        inner = json.loads(out)
        srcs = json.loads(inner) if isinstance(inner, str) else inner
    except json.JSONDecodeError:
        return None
    if not srcs:
        return None
    leitor_url = srcs[0]
    parsed = urllib.parse.urlparse(leitor_url)
    qs = urllib.parse.parse_qs(parsed.query)
    file_arg = qs.get("file", [None])[0]
    if not file_arg:
        return None
    pdf_parsed = urllib.parse.urlparse(file_arg)
    path_encoded = urllib.parse.quote(pdf_parsed.path, safe="/")
    return urllib.parse.urlunparse(pdf_parsed._replace(path=path_encoded))


def safe_pdf_name(chapter_titulo: str, original_url: str) -> str:
    """Gera nome amigável para o PDF baixado."""
    base = urllib.parse.unquote(Path(urllib.parse.urlparse(original_url).path).name)
    base = re.sub(r"[^\w.()\- ]+", "_", base, flags=re.UNICODE).strip()
    if not base.lower().endswith(".pdf"):
        base = f"{slugify(chapter_titulo)}.pdf"
    return base


# ---------- captura por capítulo ----------
def capture_chapter_ebook(chapter: ChapterInfo, out_dir: Path, cookie_jar: Path) -> None:
    if not chapter.url_ebook:
        chapter.erros.append("sem url_ebook")
        return
    print(f"        - {chapter.titulo[:70]}", flush=True)
    try:
        pdf_url = extract_pdf_url_from_viewer(chapter.url_ebook)
        if not pdf_url:
            chapter.erros.append("PDF iframe não encontrado")
            print("          ! PDF não encontrado", flush=True)
            return
        dest = out_dir / safe_pdf_name(chapter.titulo, pdf_url)
        size = http_download(pdf_url, dest, cookie_jar, referer=chapter.url_ebook)
        chapter.pdf_file = dest.name
        chapter.pdf_size_bytes = size
        chapter.captured_at = datetime.now().isoformat(timespec="seconds")
        kb = size // 1024
        print(f"          ✓ {dest.name} ({kb} KB)", flush=True)
    except Exception as exc:
        chapter.erros.append(str(exc))
        print(f"          ! erro PDF: {exc}", flush=True)


def capture_chapter_assets(chapter: ChapterInfo, out_dir: Path, cookie_jar: Path) -> None:
    if not chapter.url_assets:
        return
    try:
        url = chapter.url_assets
        base = urllib.parse.unquote(Path(urllib.parse.urlparse(url).path).name) or "assets.zip"
        dest = out_dir / base
        size = http_download(url, dest, cookie_jar, referer=PORTAL_URL)
        chapter.assets_file = dest.name
        print(f"          ✓ assets {dest.name} ({size // 1024} KB)", flush=True)
    except Exception as exc:
        chapter.erros.append(f"assets: {exc}")
        print(f"          ! erro assets: {exc}", flush=True)


def capture_chapter_slides(chapter: ChapterInfo, out_dir: Path, max_slides: int = 30) -> None:
    if not chapter.url_conteudo:
        chapter.erros.append("sem url_conteudo")
        return
    slides_dir = out_dir / "slides"
    slides_dir.mkdir(parents=True, exist_ok=True)
    chapter.slides_dir = "slides"
    try:
        goto(chapter.url_conteudo)
        time.sleep(2)
        slides: list[dict] = []
        for idx in range(1, max_slides + 1):
            snap = snapshot(interactive=False, urls=True)
            sdir = slides_dir / f"slide{idx:02d}"
            sdir.mkdir(parents=True, exist_ok=True)
            (sdir / "snapshot.txt").write_text(snap, encoding="utf-8")
            (sdir / "content.md").write_text(snapshot_to_markdown(snap), encoding="utf-8")
            try:
                screenshot(sdir / "screenshot.png", full=True)
            except AgentBrowserError as exc:
                chapter.erros.append(f"slide{idx} screenshot: {exc}")
            slides.append({"slide": idx, "iframes": collect_iframes(snap)})
            m = NEXT_SLIDE_RE.search(snap)
            if not m or "disabled" in (m.group("state") or ""):
                break
            try:
                click(m.group("ref"))
                time.sleep(1.2)
            except AgentBrowserError as exc:
                chapter.erros.append(f"slide{idx} click: {exc}")
                break
        # markdown consolidado
        md = "\n\n---\n\n".join(
            (slides_dir / f"slide{s['slide']:02d}" / "content.md").read_text(encoding="utf-8")
            for s in slides
        )
        (out_dir / "conteudo.md").write_text(
            f"# {chapter.titulo}\n\n_URL_: {chapter.url_conteudo}\n\n---\n\n{md}\n",
            encoding="utf-8",
        )
    except Exception as exc:
        chapter.erros.append(f"slides: {exc}")
        print(f"          ! erro slides: {exc}", flush=True)


# ---------- orquestrador ----------
def _phase_number(label: str) -> str:
    m = re.search(r"\d+", label)
    return m.group(0) if m else ""


PHASE_HEADER_RE = re.compile(r'"\s*Fase\s+(\d+)\s*-\s*([^"\n]+?)\s*"', re.IGNORECASE)


def _extract_active_phase_header(snap: str) -> Optional[tuple[str, str]]:
    """Extrai (numero, tema) da fase ativa no snapshot.

    Procura por strings tipo 'Fase 3 - Colheita De Dados E Insights' em
    StaticText/headings logo abaixo do bloco de botões FASE.
    """
    for m in PHASE_HEADER_RE.finditer(snap):
        # Ignora ocorrências dentro de URLs / nomes de arquivo (pluginfile, etc.)
        ctx_start = max(0, m.start() - 40)
        ctx = snap[ctx_start:m.end() + 5]
        if "pluginfile" in ctx or "conteudospdf" in ctx or ".pdf" in ctx:
            continue
        return m.group(1), m.group(2).strip()
    return None


def _wait_phase_content(phase_label: str, before_header: Optional[tuple[str, str]],
                         max_wait_s: float = 10.0) -> tuple[str, Optional[tuple[str, str]]]:
    """Após clicar num botão de FASE, aguarda o heading 'Fase N - Tema' mudar.

    Retorna (snapshot, header_atual).
    """
    target_num = _phase_number(phase_label)
    deadline = time.time() + max_wait_s
    snap = ""
    cur_header: Optional[tuple[str, str]] = None
    while time.time() < deadline:
        snap = snapshot(interactive=True, urls=True)
        cur_header = _extract_active_phase_header(snap)
        if cur_header and cur_header[0] == target_num:
            return snap, cur_header
        if cur_header and before_header and cur_header != before_header:
            return snap, cur_header
        time.sleep(0.6)
    return snap, cur_header


def _dismiss_modals() -> None:
    try:
        eval_js(
            "(()=>{const sels=['button[aria-label=\"Fechar\"]','button.close','[role=dialog] button']"
            ";for(const s of sels){const b=document.querySelector(s);if(b){b.click();return s;}}return null;})()"
        )
        time.sleep(0.3)
    except AgentBrowserError:
        pass


def capture_phase(label: str, ref: str, out_dir: Path, cookie_jar: Path,
                  modes: dict, max_chapters: Optional[int],
                  seen_ebook_urls: set[str]) -> PhaseInfo:
    print(f"\n[Fase] {label}", flush=True)
    _dismiss_modals()
    # Captura header atual ANTES de clicar para detectar mudança
    pre_snap = snapshot(interactive=True, urls=True)
    before_header = _extract_active_phase_header(pre_snap)
    if before_header:
        print(f"   (header antes do clique: Fase {before_header[0]} - {before_header[1]})", flush=True)

    click(ref)
    ab("wait", "--load", "networkidle", timeout=15, check=False)
    _dismiss_modals()

    out_dir.mkdir(parents=True, exist_ok=True)
    snap, after_header = _wait_phase_content(label, before_header)
    target_num = _phase_number(label)
    if after_header:
        match = "✓" if after_header[0] == target_num else "≠"
        print(f"   (header após clique : Fase {after_header[0]} - {after_header[1]} [{match}])", flush=True)
    (out_dir / "home_snapshot.txt").write_text(snap, encoding="utf-8")
    try:
        screenshot(out_dir / "home.png", full=True)
    except AgentBrowserError as exc:
        print(f"  ! screenshot fase: {exc}", flush=True)

    chapters, extras, entregas = parse_phase_snapshot(snap)

    info = PhaseInfo(
        nome=label,
        url=page_url(),
        titulo_pagina=page_title(),
        links_extras=extras,
        entregas=entregas,
        captured_at=datetime.now().isoformat(timespec="seconds"),
    )

    # Caso 1: header não trocou para a fase correta → portal mostrou fallback
    if after_header and after_header[0] != target_num:
        info.bloqueada = True
        info.observacao = (
            f"Fase indisponível: portal continuou mostrando 'Fase {after_header[0]} - "
            f"{after_header[1]}' após clicar em {label}."
        )
        print(f"   ⨯ {label} indisponível — portal exibiu Fase {after_header[0]}.", flush=True)
        (out_dir / "INDEX.json").write_text(
            json.dumps(asdict(info), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return info

    # Caso 2: 100% dos capítulos com e-book já visto antes (dedupe defensivo)
    chapters_with_ebook = [c for c in chapters if c.url_ebook]
    duplicates = [c for c in chapters_with_ebook if c.url_ebook in seen_ebook_urls]
    if chapters_with_ebook and len(duplicates) == len(chapters_with_ebook):
        info.bloqueada = True
        info.observacao = (
            "Todos os capítulos já foram baixados em fase anterior (provável fallback)."
        )
        print(f"   ⨯ {label} bloqueada — capítulos são duplicatas; nada a baixar.", flush=True)
        (out_dir / "INDEX.json").write_text(
            json.dumps(asdict(info), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return info

    # Caso 3: snapshot não traz nenhum capítulo (fase ainda não liberada)
    if not chapters:
        info.bloqueada = True
        info.observacao = (
            "Nenhum capítulo retornado para esta fase (provavelmente ainda não liberada)."
        )
        print(f"   ⨯ {label} sem capítulos — fase ainda não liberada.", flush=True)
        (out_dir / "INDEX.json").write_text(
            json.dumps(asdict(info), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return info

    if max_chapters:
        chapters = chapters[:max_chapters]

    print(f"   {len(chapters)} capítulo(s) | {len(entregas)} entregas | {len(extras)} extras", flush=True)

    for idx, ch in enumerate(chapters, start=1):
        if ch.url_ebook and ch.url_ebook in seen_ebook_urls:
            ch.erros.append("duplicado de fase anterior; pulado")
            print(f"        - {ch.titulo[:70]} (duplicado, pulado)", flush=True)
            info.capitulos.append(ch)
            continue
        ch_dir = out_dir / f"cap{idx:02d}_{slugify(ch.titulo)[:40]}"
        ch_dir.mkdir(parents=True, exist_ok=True)
        if modes["pdf"]:
            capture_chapter_ebook(ch, ch_dir, cookie_jar)
        if modes["assets"]:
            capture_chapter_assets(ch, ch_dir, cookie_jar)
        if modes["slides"]:
            capture_chapter_slides(ch, ch_dir)
        if ch.url_ebook:
            seen_ebook_urls.add(ch.url_ebook)
        info.capitulos.append(ch)

    (out_dir / "INDEX.json").write_text(
        json.dumps(asdict(info), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return info


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--phases", default="", help="CSV de fases (ex: 1,3). Vazio = todas detectadas.")
    parser.add_argument("--max-chapters", type=int, default=None, help="Limita capítulos por fase.")
    parser.add_argument("--slides", action="store_true", help="Também captura HTML iterando slides (lento).")
    parser.add_argument("--assets", action="store_true", help="Também baixa ZIPs de assets quando houver.")
    parser.add_argument("--no-pdf", action="store_true", help="Desativa download de PDFs (use só com --slides).")
    parser.add_argument("--keep-output", action="store_true", help="Não apaga capturas anteriores.")
    args = parser.parse_args()

    if args.no_pdf and not (args.slides or args.assets):
        print("Erro: --no-pdf precisa de --slides e/ou --assets.", file=sys.stderr)
        return 2

    _ensure_key()
    if shutil.which("agent-browser") is None:
        print("Erro: agent-browser não está no PATH.", file=sys.stderr)
        return 2
    if shutil.which("curl") is None:
        print("Erro: curl é obrigatório para download dos PDFs.", file=sys.stderr)
        return 2

    if not args.keep_output and OUTPUT_DIR.exists():
        print(f"Limpando {OUTPUT_DIR} (use --keep-output para preservar).", flush=True)
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    modes = {"pdf": not args.no_pdf, "slides": args.slides, "assets": args.assets}
    cookie_jar = OUTPUT_DIR / ".cookies.txt"

    try:
        login()
        goto(PORTAL_URL)
        snap = snapshot(interactive=True, urls=True)
        (OUTPUT_DIR / "portal_snapshot.txt").write_text(snap, encoding="utf-8")
        try:
            screenshot(OUTPUT_DIR / "portal_home.png", full=True)
        except AgentBrowserError as exc:
            print(f"  ! screenshot portal: {exc}", flush=True)

        cookie_jar.write_text(get_cookies_netscape(), encoding="utf-8")
        os.chmod(cookie_jar, 0o600)

        phases = PHASE_BUTTON_RE.findall(snap)
        if not phases:
            print("Nenhum botão FASE detectado.", file=sys.stderr)
            return 3

        wanted = {f"FASE {n.strip()}" for n in args.phases.split(",") if n.strip()} if args.phases else set()
        print(f"\nFases detectadas: {[p[0] for p in phases]}", flush=True)

        all_phases: list[PhaseInfo] = []
        seen_ebook_urls: set[str] = set()
        for label, ref in phases:
            if wanted and label not in wanted:
                continue
            goto(PORTAL_URL)
            snap2 = snapshot(interactive=True, urls=True)
            phase_ref = dict(PHASE_BUTTON_RE.findall(snap2)).get(label, ref)
            phase_dir = OUTPUT_DIR / slugify(label.lower().replace(" ", ""))
            info = capture_phase(label, phase_ref, phase_dir, cookie_jar, modes,
                                 args.max_chapters, seen_ebook_urls)
            all_phases.append(info)
            cookie_jar.write_text(get_cookies_netscape(), encoding="utf-8")

        index_path = OUTPUT_DIR / "INDEX.json"
        new_phase_data = {p.nome: asdict(p) for p in all_phases}
        merged_phases: dict[str, dict] = {}
        if args.keep_output and index_path.exists():
            try:
                prev = json.loads(index_path.read_text(encoding="utf-8"))
                for p in prev.get("phases", []):
                    merged_phases[p["nome"]] = p
            except (json.JSONDecodeError, OSError):
                pass
        merged_phases.update(new_phase_data)
        ordered = sorted(merged_phases.values(), key=lambda p: p["nome"])
        index = {
            "captured_at": datetime.now().isoformat(timespec="seconds"),
            "portal_url": PORTAL_URL,
            "modes": modes,
            "phases": ordered,
        }
        index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

        print(f"\nCaptura concluída. Resumo em {OUTPUT_DIR / 'INDEX.json'}")
        for p in all_phases:
            if p.bloqueada:
                print(f"  {p.nome}: BLOQUEADA / não liberada (sem download)")
                continue
            ok_count = sum(1 for c in p.capitulos if c.pdf_file)
            err_count = sum(1 for c in p.capitulos if c.erros)
            print(f"  {p.nome}: {len(p.capitulos)} caps | {ok_count} PDFs ok | {err_count} com avisos")
    finally:
        try:
            if cookie_jar.exists():
                cookie_jar.unlink()
        except OSError:
            pass
        close_all()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
