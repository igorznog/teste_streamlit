#!/usr/bin/env python3
"""Coleta profunda das entregas (assignments e quizzes) de uma fase FIAP.

Lê `docs/validation/captures/fases/fase<N>/INDEX.json` (gerado por
`fiap_capture_all_phases.py`) e, para cada URL de entrega, captura:

  - Metadados (título, prazo, tipo individual/grupo, status, participantes do grupo).
  - Enunciado completo em HTML (innerHTML do container principal) + versão Markdown.
  - Screenshot full-page.
  - Anexos linkados (PDFs, DOCX, ZIPs) baixados via cookies+Referer.
  - Para quizzes: número de tentativas, restrições — sem iniciar a prova.

Saída em `docs/validation/captures/fases/fase<N>/tasks/task<NN>_<slug>/`.

Uso:
    python3 scripts/fiap_capture_phase_tasks.py --phase 3
    python3 scripts/fiap_capture_phase_tasks.py --phase 3 --tasks 1,2  # subset
    python3 scripts/fiap_capture_phase_tasks.py --phase 3 --no-attachments
"""

from __future__ import annotations

import argparse
import html as html_lib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

# Reusa o que já está pronto no orquestrador de fases.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fiap_capture_all_phases import (  # noqa: E402
    AgentBrowserError,
    OUTPUT_DIR as PHASES_OUTPUT_DIR,
    SESSION_NAME,
    USER_AGENT,
    _dismiss_modals,
    _ensure_key,
    ab,
    close_all,
    eval_js,
    get_cookies_netscape,
    goto,
    http_download,
    login,
    page_title,
    page_url,
    safe_pdf_name,
    screenshot,
    slugify,
    snapshot,
)

ROOT = Path(__file__).resolve().parent.parent

# Padrões que aparecem no header das entregas (FIAP customizou em cima do Moodle)
DATE_RE = re.compile(r"DE\s+(\d{2}/\d{2}/\d{4})\s+A\s+(\d{2}/\d{2}/\d{4})", re.IGNORECASE)
STATUS_KEYWORDS = [
    ("PRAZO ENCERRADO", "prazo_encerrado"),
    ("ENTREGA PENDENTE", "pendente"),
    ("ENTREGUE", "entregue"),
    ("CONCLUÍDO", "concluido"),
    ("AVALIADO", "avaliado"),
    ("PENDENTE", "pendente"),
]
TYPE_KEYWORDS = [
    ("ATIVIDADE EM GRUPO", "grupo"),
    ("ATIVIDADE INDIVIDUAL", "individual"),
    ("QUESTIONÁRIO INDIVIDUAL", "quiz_individual"),
    ("QUESTIONÁRIO EM GRUPO", "quiz_grupo"),
]
ATTACHMENT_EXT_RE = re.compile(r"\.(pdf|docx?|pptx?|xlsx?|zip|rar|csv|ipynb|txt)(\?|$)", re.IGNORECASE)


@dataclass
class TaskCapture:
    indice: int
    url: str
    moodle_id: Optional[str] = None
    moodle_mod: Optional[str] = None  # "assign" | "quiz"
    titulo: Optional[str] = None
    pagina_titulo: Optional[str] = None
    tipo: Optional[str] = None
    data_inicio: Optional[str] = None
    data_fim: Optional[str] = None
    status: Optional[str] = None
    pode_entregar: bool = False
    participantes_grupo: list[str] = field(default_factory=list)
    tentativas_quiz: Optional[str] = None
    anexos: list[dict] = field(default_factory=list)
    links_externos: list[str] = field(default_factory=list)
    enunciado_md_file: Optional[str] = None
    enunciado_html_file: Optional[str] = None
    snapshot_file: Optional[str] = None
    screenshot_file: Optional[str] = None
    rubricas_csv_file: Optional[str] = None
    captured_at: Optional[str] = None
    erros: list[str] = field(default_factory=list)


def parse_url(url: str) -> tuple[Optional[str], Optional[str]]:
    """Extrai (mod, id) de /mod/<mod>/view.php?id=<N>."""
    parsed = urllib.parse.urlparse(url)
    m = re.search(r"/mod/([^/]+)/", parsed.path)
    mod = m.group(1) if m else None
    qs = urllib.parse.parse_qs(parsed.query)
    mid = qs.get("id", [None])[0]
    return mod, mid


def detect_period(text: str) -> tuple[Optional[str], Optional[str]]:
    m = DATE_RE.search(text)
    if m:
        return m.group(1), m.group(2)
    return None, None


def detect_status(text: str) -> Optional[str]:
    upper = text.upper()
    for keyword, slug in STATUS_KEYWORDS:
        if keyword in upper:
            return slug
    return None


def detect_type(text: str) -> Optional[str]:
    upper = text.upper()
    for keyword, slug in TYPE_KEYWORDS:
        if keyword in upper:
            return slug
    return None


def normalize_attachment_url(url: str) -> str:
    """Trata URLs de pluginfile (decodifica espaços/acentos e re-encoda path)."""
    parsed = urllib.parse.urlparse(url)
    decoded_path = urllib.parse.unquote(parsed.path)
    encoded_path = urllib.parse.quote(decoded_path, safe="/")
    return urllib.parse.urlunparse(parsed._replace(path=encoded_path))


def attachment_filename(url: str, fallback: str) -> str:
    base = urllib.parse.unquote(Path(urllib.parse.urlparse(url).path).name)
    if not base or base == "/":
        return fallback
    return re.sub(r"[^\w.()\- ]+", "_", base, flags=re.UNICODE).strip() or fallback


def extract_main_html() -> str:
    """Pega o HTML do container principal Moodle (`#region-main`).

    Fallback para `[role=main]` e depois `body`.
    """
    js = (
        "(()=>{const el=document.querySelector('#region-main')"
        "||document.querySelector('[role=main]')"
        "||document.body;return el?el.innerHTML:'';})()"
    )
    raw = eval_js(js)
    # eval pode vir como JSON-string quoted; tenta desempacotar
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return raw


def extract_text_blocks() -> list[str]:
    """Texto visível do container principal, partido em blocos lógicos."""
    js = (
        "(()=>{const el=document.querySelector('#region-main')"
        "||document.querySelector('[role=main]')||document.body;"
        "if(!el)return [];"
        "return Array.from(el.querySelectorAll('p,li,h1,h2,h3,h4,td,th,div'))"
        ".map(n=>n.innerText.trim()).filter(s=>s.length>0);})()"
    )
    raw = eval_js(js)
    try:
        loaded = json.loads(raw)
        return json.loads(loaded) if isinstance(loaded, str) else loaded
    except (json.JSONDecodeError, ValueError):
        return []


def extract_attachments() -> list[dict]:
    """Lista links que parecem anexos baixáveis (pdf/docx/zip/etc.) no main."""
    js = (
        "(()=>{const el=document.querySelector('#region-main')"
        "||document.querySelector('[role=main]')||document.body;"
        "if(!el)return [];"
        "return Array.from(el.querySelectorAll('a[href]')).map(a=>({"
        "href:a.href,"
        "text:(a.innerText||a.title||'').trim().slice(0,200)}));})()"
    )
    raw = eval_js(js)
    try:
        loaded = json.loads(raw)
        items = json.loads(loaded) if isinstance(loaded, str) else loaded
    except (json.JSONDecodeError, ValueError):
        return []
    result, seen = [], set()
    for item in items:
        href = item.get("href", "")
        if not href or href.startswith("#") or "javascript:" in href:
            continue
        if href in seen:
            continue
        if ATTACHMENT_EXT_RE.search(href) or "pluginfile.php" in href:
            seen.add(href)
            result.append({"url": href, "text": item.get("text", "")})
    return result


def extract_external_links() -> list[str]:
    js = (
        "(()=>{const el=document.querySelector('#region-main')"
        "||document.querySelector('[role=main]')||document.body;"
        "if(!el)return [];"
        "return Array.from(el.querySelectorAll('a[href]'))"
        ".map(a=>a.href)"
        ".filter(h=>h&&!h.startsWith('#')&&!h.includes('javascript:'));})()"
    )
    raw = eval_js(js)
    try:
        loaded = json.loads(raw)
        items = json.loads(loaded) if isinstance(loaded, str) else loaded
    except (json.JSONDecodeError, ValueError):
        return []
    return [
        h for h in items
        if "on.fiap.com.br" not in h and not ATTACHMENT_EXT_RE.search(h)
    ]


def extract_group_participants() -> list[str]:
    """Para tasks de grupo, lista nomes dos participantes confirmados."""
    js = (
        "(()=>{const el=document.querySelector('#region-main')"
        "||document.body;if(!el)return [];"
        "const items=Array.from(el.querySelectorAll('li,span,div'))"
        ".map(n=>n.innerText.trim()).filter(s=>s.length>2 && s.length<120);"
        "const set=new Set();"
        "for(const t of items){if(/RM\\s*\\d|^[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-zà-úA-ZÀ-Ú\\s]{4,80}$/.test(t))set.add(t);}"
        "return Array.from(set).slice(0,30);})()"
    )
    raw = eval_js(js)
    try:
        loaded = json.loads(raw)
        items = json.loads(loaded) if isinstance(loaded, str) else loaded
        return [s for s in items if isinstance(s, str)]
    except (json.JSONDecodeError, ValueError):
        return []


def expand_introduction_section() -> None:
    """Algumas seções 'Introdução' começam colapsadas; clica para expandir."""
    js = (
        "(()=>{const candidates=document.querySelectorAll("
        "'[aria-expanded=\"false\"], details:not([open]), .collapsible:not(.show)');"
        "let n=0;candidates.forEach(c=>{try{c.click&&c.click();n++;}catch(e){}});"
        "return n;})()"
    )
    try:
        eval_js(js)
        time.sleep(0.5)
    except AgentBrowserError:
        pass


def html_to_markdown(html: str) -> str:
    """Conversão pragmática HTML→Markdown (sem dependências externas)."""
    text = html
    text = re.sub(r"(?is)<script.*?</script>", "", text)
    text = re.sub(r"(?is)<style.*?</style>", "", text)
    text = re.sub(r"(?is)<br\s*/?>", "\n", text)
    text = re.sub(r"(?is)</(p|div|li|tr|h[1-6])\s*>", "\n", text)
    text = re.sub(r"(?is)<li[^>]*>", "- ", text)
    text = re.sub(r"(?is)<h1[^>]*>", "\n# ", text)
    text = re.sub(r"(?is)<h2[^>]*>", "\n## ", text)
    text = re.sub(r"(?is)<h3[^>]*>", "\n### ", text)
    text = re.sub(r"(?is)<h4[^>]*>", "\n#### ", text)
    text = re.sub(r"(?is)<td[^>]*>", " | ", text)
    text = re.sub(r"(?is)<th[^>]*>", " | ", text)
    text = re.sub(r"(?is)<a[^>]*href=\"([^\"]+)\"[^>]*>(.*?)</a>", r"[\2](\1)", text)
    text = re.sub(r"(?is)<strong[^>]*>(.*?)</strong>", r"**\1**", text)
    text = re.sub(r"(?is)<b[^>]*>(.*?)</b>", r"**\1**", text)
    text = re.sub(r"(?is)<em[^>]*>(.*?)</em>", r"*\1*", text)
    text = re.sub(r"(?is)<i[^>]*>(.*?)</i>", r"*\1*", text)
    text = re.sub(r"(?is)<[^>]+>", "", text)
    text = html_lib.unescape(text)
    # Limpa linhas duplicadas e espaços
    lines = [ln.strip() for ln in text.splitlines()]
    out: list[str] = []
    blank = 0
    for ln in lines:
        if not ln:
            blank += 1
            if blank <= 1:
                out.append("")
            continue
        blank = 0
        out.append(re.sub(r"\s+", " ", ln))
    return "\n".join(out).strip() + "\n"


def extract_rubric_table() -> Optional[str]:
    """Se houver tabela(s) tipo 'Critério | Descrição | Pontos', retorna como CSV."""
    js = (
        "(()=>{const tables=Array.from(document.querySelectorAll('table'));"
        "const out=[];for(const t of tables){"
        "const rows=Array.from(t.querySelectorAll('tr'));"
        "const text=rows.map(r=>Array.from(r.querySelectorAll('th,td'))"
        ".map(c=>c.innerText.replace(/\\n+/g,' ').trim())).filter(r=>r.length>0);"
        "if(text.length>1 && text[0].some(c=>/crit|pont/i.test(c))){out.push(text);}}"
        "return out;})()"
    )
    raw = eval_js(js)
    try:
        loaded = json.loads(raw)
        tables = json.loads(loaded) if isinstance(loaded, str) else loaded
    except (json.JSONDecodeError, ValueError):
        return None
    if not tables:
        return None
    csv_lines = []
    for ti, table in enumerate(tables):
        if ti > 0:
            csv_lines.append("")
        for row in table:
            csv_lines.append(",".join(f"\"{(c or '').replace(chr(34),' ')}\"" for c in row))
    return "\n".join(csv_lines) + "\n"


def detect_can_submit(snap: str) -> bool:
    return "ENTREGAR ATIVIDADE" in snap or "RESPONDER AGORA" in snap


def detect_quiz_attempts(text: str) -> Optional[str]:
    m = re.search(r"máximo de\s+(\d+)\s+tentativa", text, flags=re.IGNORECASE)
    if m:
        return f"máximo {m.group(1)} tentativa(s)"
    if "RESPONDER AGORA" in text.upper():
        return "permitido responder"
    return None


def capture_task(idx: int, url: str, out_dir: Path,
                 cookie_jar: Path, download_attachments: bool) -> TaskCapture:
    mod, mid = parse_url(url)
    task = TaskCapture(indice=idx, url=url, moodle_mod=mod, moodle_id=mid)
    print(f"\n[Task {idx}] {url}", flush=True)
    try:
        goto(url)
        time.sleep(1.0)
        _dismiss_modals()
        expand_introduction_section()

        task.pagina_titulo = page_title()
        snap = snapshot(interactive=True, urls=True)
        task.snapshot_file = "snapshot.txt"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "snapshot.txt").write_text(snap, encoding="utf-8")

        # Heading principal (assign): a generic abaixo do breadcrumb
        m = re.search(r'^- heading "([^"]+)" \[level=1', snap, flags=re.MULTILINE)
        if m:
            task.titulo = m.group(1).strip()
        else:
            m = re.search(r'Tarefa:\s*(.+?)$', task.pagina_titulo or "", flags=re.MULTILINE)
            task.titulo = (m.group(1).strip() if m else task.pagina_titulo)

        text_blocks = extract_text_blocks()
        joined = "\n".join(text_blocks)
        task.tipo = detect_type(joined) or detect_type(snap)
        task.status = detect_status(joined) or detect_status(snap)
        task.data_inicio, task.data_fim = detect_period(joined)
        task.pode_entregar = detect_can_submit(snap)
        task.tentativas_quiz = detect_quiz_attempts(joined) if mod == "quiz" else None

        # Tira screenshot apenas DEPOIS de expandir introdução
        try:
            shot_path = out_dir / "screenshot.png"
            screenshot(shot_path, full=True)
            task.screenshot_file = "screenshot.png"
        except AgentBrowserError as exc:
            task.erros.append(f"screenshot: {exc}")

        if mod == "assign":
            html = extract_main_html()
            (out_dir / "enunciado.html").write_text(html, encoding="utf-8")
            task.enunciado_html_file = "enunciado.html"
            md = html_to_markdown(html)
            (out_dir / "enunciado.md").write_text(
                f"# {task.titulo or 'Atividade'}\n\n_URL_: {url}\n\n---\n\n{md}",
                encoding="utf-8",
            )
            task.enunciado_md_file = "enunciado.md"
            rubric = extract_rubric_table()
            if rubric:
                (out_dir / "rubricas.csv").write_text(rubric, encoding="utf-8")
                task.rubricas_csv_file = "rubricas.csv"
            task.participantes_grupo = extract_group_participants() if task.tipo == "grupo" else []

            anexos = extract_attachments()
            task.links_externos = extract_external_links()
            if download_attachments and anexos:
                anexos_dir = out_dir / "anexos"
                anexos_dir.mkdir(exist_ok=True)
                for a in anexos:
                    a_url = normalize_attachment_url(a["url"])
                    fname = attachment_filename(a_url, f"anexo_{len(task.anexos)+1}")
                    dest = anexos_dir / fname
                    try:
                        size = http_download(a_url, dest, cookie_jar, referer=url)
                        task.anexos.append({
                            "url": a["url"], "arquivo": f"anexos/{fname}",
                            "tamanho_bytes": size, "rotulo": a.get("text", ""),
                        })
                        print(f"   anexo ✓ {fname} ({size // 1024} KB)", flush=True)
                    except Exception as exc:
                        task.anexos.append({
                            "url": a["url"], "arquivo": None,
                            "tamanho_bytes": 0, "erro": str(exc),
                            "rotulo": a.get("text", ""),
                        })
                        print(f"   anexo ! {fname}: {exc}", flush=True)
            else:
                task.anexos = [
                    {"url": a["url"], "arquivo": None, "rotulo": a.get("text", "")}
                    for a in anexos
                ]
        elif mod == "quiz":
            # Para quiz só capturamos metadados — NÃO clicamos em "Responder Agora".
            (out_dir / "enunciado.md").write_text(
                f"# {task.titulo or 'Quiz'}\n\n_URL_: {url}\n\n---\n\n"
                f"Tipo: {task.tipo}\n\nTentativas: {task.tentativas_quiz}\n\n"
                f"Status: {task.status}\n\nPrazo: {task.data_inicio} → {task.data_fim}\n",
                encoding="utf-8",
            )
            task.enunciado_md_file = "enunciado.md"

        task.captured_at = datetime.now().isoformat(timespec="seconds")
        print(f"   ✓ '{task.titulo}' [{task.tipo or '?'} | {task.status or '?'}"
              f" | {task.data_inicio or '?'} → {task.data_fim or '?'}]"
              f" anexos={len(task.anexos)}", flush=True)
    except Exception as exc:
        task.erros.append(str(exc))
        print(f"   ! erro: {exc}", flush=True)
    return task


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--phase", type=int, default=3, help="Número da fase (default: 3).")
    parser.add_argument("--tasks", default="", help="CSV de índices a capturar (1-based). Vazio = todas.")
    parser.add_argument("--no-attachments", action="store_true", help="Não baixar anexos.")
    parser.add_argument("--keep-output", action="store_true", help="Preservar tasks/ existentes.")
    args = parser.parse_args()

    _ensure_key()
    if shutil.which("agent-browser") is None:
        print("Erro: agent-browser não está no PATH.", file=sys.stderr)
        return 2

    phase_dir = PHASES_OUTPUT_DIR / f"fase{args.phase}"
    phase_index = phase_dir / "INDEX.json"
    if not phase_index.exists():
        print(f"Erro: {phase_index} não existe. Rode primeiro: "
              f"python3 scripts/fiap_capture_all_phases.py --phases {args.phase}",
              file=sys.stderr)
        return 3

    phase_data = json.loads(phase_index.read_text(encoding="utf-8"))
    entregas = phase_data.get("entregas", [])
    if not entregas:
        print(f"Nenhuma entrega registrada em {phase_index}.", file=sys.stderr)
        return 0

    wanted = {int(i) for i in args.tasks.split(",") if i.strip().isdigit()} if args.tasks else set()

    tasks_dir = phase_dir / "tasks"
    if not args.keep_output and tasks_dir.exists():
        # Remove apenas subdirs taskNN_* deixando snapshots antigos intocados
        for entry in list(tasks_dir.iterdir()):
            if entry.is_dir() and entry.name.startswith("task"):
                shutil.rmtree(entry)
    tasks_dir.mkdir(parents=True, exist_ok=True)

    cookie_jar = tasks_dir / ".cookies.txt"

    try:
        login()
        # Aquece a sessão visitando o portal antes de exportar cookies.
        goto("https://on.fiap.com.br/local/conteudocurso/")
        time.sleep(1.0)
        cookie_jar.write_text(get_cookies_netscape(), encoding="utf-8")
        os.chmod(cookie_jar, 0o600)

        captures: list[TaskCapture] = []
        for idx, entrega in enumerate(entregas, start=1):
            if wanted and idx not in wanted:
                continue
            mod, mid = parse_url(entrega["url"])
            slug_seed = f"task{idx:02d}_{mod or 'item'}_{mid or 'x'}"
            task_dir = tasks_dir / slug_seed
            cap = capture_task(idx, entrega["url"], task_dir,
                               cookie_jar, not args.no_attachments)
            # Renomeia pasta usando o título descoberto, se houver
            if cap.titulo:
                pretty = tasks_dir / f"task{idx:02d}_{slugify(cap.titulo)[:48]}"
                if pretty != task_dir and pretty.exists():
                    shutil.rmtree(pretty)
                if pretty != task_dir:
                    task_dir.rename(pretty)
                    task_dir = pretty
            (task_dir / "meta.json").write_text(
                json.dumps(asdict(cap), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            captures.append(cap)

        # INDEX agregado de tasks
        tasks_index = {
            "captured_at": datetime.now().isoformat(timespec="seconds"),
            "phase": args.phase,
            "tasks": [asdict(c) for c in captures],
        }
        (tasks_dir / "INDEX.json").write_text(
            json.dumps(tasks_index, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        print("\nResumo das tasks capturadas:")
        for c in captures:
            print(f"  [{c.indice}] {c.titulo or c.pagina_titulo}")
            print(f"      tipo={c.tipo} status={c.status}"
                  f" prazo={c.data_inicio}→{c.data_fim} anexos={len(c.anexos)}")
            if c.erros:
                print(f"      ⚠ {c.erros}")
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
