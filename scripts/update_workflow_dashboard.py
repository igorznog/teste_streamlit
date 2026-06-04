#!/usr/bin/env python3
"""Gera dashboards HTML estáticos a partir de TASK_REGISTRY.md e GROUP.md.

Os HTMLs são artefatos de leitura rápida para o grupo. A fonte de verdade
continua sendo o Markdown versionado no repositório.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "TASK_REGISTRY.md"
GROUP_PATH = ROOT / "GROUP.md"
DASHBOARD_DIR = ROOT / "docs" / "dashboard"
SOURCE_SIGNATURE = ""


@dataclass
class Member:
    name: str
    rm: str
    github: str
    responsibility: str


@dataclass
class Task:
    number: int
    title: str
    block: str
    status: str = "Status não informado"
    mode: str = ""
    folder: str = ""
    spec: str = ""
    deadline: str = ""
    portal_url: str = ""
    discipline: str = ""
    checked: int = 0
    unchecked: int = 0
    pending: list[str] = field(default_factory=list)
    deliverables: list[str] = field(default_factory=list)

    @property
    def progress(self) -> int:
        total = self.checked + self.unchecked
        if total:
            return round((self.checked / total) * 100)
        label = normalize(self.status)
        if any(word in label for word in ["concluida", "pronta", "importada"]):
            return 100
        if "em andamento" in label:
            return 55
        return 0

    @property
    def status_kind(self) -> str:
        label = normalize(self.status)
        if any(word in label for word in ["nao iniciada", "prazo encerrado"]):
            return "danger"
        if any(word in label for word in ["em andamento", "aguardando", "pendente"]):
            return "warning"
        if any(word in label for word in ["concluida", "pronta", "importada", "historica"]):
            return "success"
        return "info"

    @property
    def is_workflow_development(self) -> bool:
        return is_workflow_development_task(self)


WORKFLOW_DEV_TASK_NUMBERS = {5}
PLACEHOLDER_GROUP_LABELS = {
    "",
    "a definir",
    "definir",
    "placeholder",
    "grupo 45",
    "grupo fiap",
}


def is_workflow_development_task(task: Task) -> bool:
    if task.number in WORKFLOW_DEV_TASK_NUMBERS:
        return True
    title = normalize(task.title)
    if any(
        phrase in title
        for phrase in (
            "validacao do novo workflow",
            "validacao do workflow",
            "infra de trabalho",
        )
    ):
        return True
    folder = task.folder.replace("\\", "/").lower()
    return folder.startswith("docs/validation/")


def is_faculty_task(task: Task) -> bool:
    return not is_workflow_development_task(task)


def split_tasks(tasks: list[Task]) -> tuple[list[Task], list[Task]]:
    faculty = [task for task in tasks if is_faculty_task(task)]
    workflow = [task for task in tasks if is_workflow_development_task(task)]
    return faculty, workflow


def display_group_label(group_meta: dict[str, str]) -> str:
    raw = (group_meta.get("Nome ou número do grupo") or "").strip()
    if normalize(raw) in PLACEHOLDER_GROUP_LABELS:
        return "FIAP Group (número a definir)"
    return raw


def display_project_label(group_meta: dict[str, str]) -> str:
    return (
        group_meta.get("Nome curto do projeto")
        or group_meta.get("Disciplina / módulo")
        or "FIAP Academic Workflow"
    ).strip()


def normalize(value: str) -> str:
    table = str.maketrans("áàãâéêíóôõúçÁÀÃÂÉÊÍÓÔÕÚÇ", "aaaaeeioooucAAAAEEIOOOUC")
    return value.translate(table).lower()


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def inline_md(value: str) -> str:
    text = esc(value)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"&lt;(https?://[^&]+)&gt;", r'<a href="\1">\1</a>', text)
    return text


def slug(value: str) -> str:
    clean = normalize(value)
    clean = re.sub(r"[^a-z0-9]+", "-", clean).strip("-")
    return clean or "item"


def parse_field(block: str, label: str) -> str:
    pattern = rf"^- \*\*{re.escape(label)}:\*\*\s*(.+)$"
    match = re.search(pattern, block, flags=re.MULTILINE)
    return clean_value(match.group(1)) if match else ""


def clean_value(value: str) -> str:
    value = value.strip()
    value = value.strip("`")
    if value.startswith("<") and ">" in value:
        value = value[1:value.index(">")]
    return value.strip()


def parse_tasks(text: str) -> list[Task]:
    matches = list(re.finditer(r"^## Task\s+(\d+)\s+—\s+(.+)$", text, flags=re.MULTILINE))
    tasks: list[Task] = []
    for index, match in enumerate(matches):
      start = match.start()
      end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
      block = text[start:end].strip()
      task = Task(number=int(match.group(1)), title=match.group(2).strip(), block=block)
      task.status = parse_field(block, "Status") or task.status
      task.mode = parse_field(block, "Modo")
      task.folder = parse_field(block, "Pasta")
      task.spec = parse_field(block, "Spec") or parse_field(block, "Spec aprovada") or parse_field(block, "Spec sugerida")
      task.deadline = parse_field(block, "Prazo") or parse_field(block, "Janela") or parse_field(block, "Janela original")
      task.portal_url = parse_field(block, "Portal URL")
      task.discipline = parse_field(block, "Disciplina")
      task.checked = len(re.findall(r"^\s*-\s+\[x\]", block, flags=re.IGNORECASE | re.MULTILINE))
      task.unchecked = len(re.findall(r"^\s*-\s+\[ \]", block, flags=re.MULTILINE))
      task.pending = extract_pending(block)
      task.deliverables = extract_deliverables(block)
      tasks.append(task)
    return tasks


def extract_pending(block: str) -> list[str]:
    items: list[str] = []
    in_pending = False
    for raw in block.splitlines():
        line = raw.strip()
        if line.startswith("### "):
            in_pending = "pendenc" in normalize(line) or "progresso" in normalize(line)
            continue
        if in_pending and line.startswith("---"):
            in_pending = False
        if in_pending:
            match = re.match(r"(?:[-*]\s+\[ \]|\d+\.)\s+(.+)", line)
            if match:
                items.append(match.group(1).strip())
        elif re.match(r"[-*]\s+\[ \]\s+", line):
            items.append(re.sub(r"^[-*]\s+\[ \]\s+", "", line))
    return items[:8]


def extract_deliverables(block: str) -> list[str]:
    items: list[str] = []
    in_deliverables = False
    for raw in block.splitlines():
        line = raw.strip()
        if line.startswith("### "):
            label = normalize(line)
            in_deliverables = "entreg" in label or "escopo" in label
            continue
        if in_deliverables:
            match = re.match(r"[-*]\s+(.+)", line)
            if match:
                items.append(match.group(1).strip())
    return items[:8]


def parse_group(text: str) -> tuple[dict[str, str], list[Member]]:
    meta: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"- \*\*(.+?):\*\*\s*(.+)", line.strip())
        if match:
            meta[match.group(1)] = match.group(2).strip()

    members: list[Member] = []
    for line in text.splitlines():
        if not line.startswith("|") or "---" in line or "Nome | RM" in line:
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) >= 4 and parts[0]:
            members.append(Member(parts[0], parts[1], parts[2], parts[3]))
    return meta, members


def collect_stats(
    faculty_tasks: list[Task],
    workflow_tasks: list[Task],
    members: list[Member],
    registry_text: str,
) -> dict[str, int]:
    active = [task for task in faculty_tasks if task.status_kind in {"warning", "danger"}]
    pdf_match = re.search(r"(\d+)\s+PDFs", registry_text)
    return {
        "tasks": len(faculty_tasks),
        "workflow_tasks": len(workflow_tasks),
        "members": len(members),
        "active": len(active),
        "ready": sum(1 for task in faculty_tasks if task.status_kind == "success"),
        "pending": sum(task.unchecked for task in faculty_tasks),
        "pdfs": int(pdf_match.group(1)) if pdf_match else 0,
        "workflows": len(list((ROOT / "docs" / "workflows").glob("*.md"))),
        "templates": len(list((ROOT / "docs" / "templates").glob("*.md"))),
        "scripts": len(list((ROOT / "scripts").glob("*.py"))),
        "knowledge": len([path for path in (ROOT / "knowledge").glob("*") if path.is_dir()]),
    }


def relative_link(path_value: str) -> str:
    if not path_value:
        return ""
    path_value = clean_value(path_value.split("—", 1)[0])
    if path_value.startswith("http"):
        return path_value
    candidate = ROOT / path_value
    if candidate.exists():
        return "../../" + path_value
    return ""


def latest_tasks(tasks: list[Task], *, faculty_only: bool = True) -> list[Task]:
    pool = [task for task in tasks if is_faculty_task(task)] if faculty_only else list(tasks)
    priority = {"warning": 0, "danger": 1, "info": 2, "success": 3}
    return sorted(pool, key=lambda item: (priority.get(item.status_kind, 9), item.number))[:6]


def html_page(title: str, body: str) -> str:
    source_signature = SOURCE_SIGNATURE or "local"
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  {STYLE}
</head>
<body>
  <main class="shell">
    {body}
    <footer class="footer">
      Gerado por <code>python scripts/update_workflow_dashboard.py</code>. Snapshot <code>{esc(source_signature)}</code>. A fonte de verdade continua sendo <code>TASK_REGISTRY.md</code> e <code>GROUP.md</code>.
    </footer>
  </main>
</body>
</html>
"""


def nav(active: str) -> str:
    links = [
        ("index", "Início", "index.html"),
        ("grupo", "Grupo", "grupo.html"),
        ("individual", "Individual", "individual.html"),
        ("registry", "Task Registry", "registry.html"),
        ("readme", "README", "../../README.md"),
    ]
    return '<nav class="topbar">' + "".join(
        f'<a class="navlink {"active" if key == active else ""}" href="{href}">{label}</a>'
        for key, label, href in links
    ) + "</nav>"


def render_metric(label: str, value: object, hint: str = "") -> str:
    return f"""<article class="metric">
  <strong>{esc(value)}</strong>
  <span>{esc(label)}</span>
  {f'<small>{esc(hint)}</small>' if hint else ''}
</article>"""


def render_task_card(task: Task, compact: bool = False) -> str:
    folder = relative_link(task.folder)
    spec = relative_link(task.spec)
    links = []
    if folder:
        links.append(f'<a href="{esc(folder)}">pasta</a>')
    if spec:
        links.append(f'<a href="{esc(spec)}">spec</a>')
    if task.portal_url:
        links.append(f'<a href="{esc(task.portal_url)}">portal</a>')
    pending = task.pending[:3]
    pending_html = "".join(f"<li>{inline_md(item)}</li>" for item in pending)
    detail = "" if compact else f"""
      <div class="card-detail">
        <p>{inline_md(task.discipline or task.mode or "Sem disciplina registrada.")}</p>
        {'<ul>' + pending_html + '</ul>' if pending_html else '<p class="muted">Sem pendências detalhadas neste bloco.</p>'}
      </div>
    """
    scope = "workflow-dev" if task.is_workflow_development else "faculty"
    scope_badge = (
        '<span class="pill info scope-pill">workflow</span>'
        if task.is_workflow_development
        else ""
    )
    return f"""<article class="task-card" data-kind="{esc(task.status_kind)}" data-scope="{scope}" data-title="{esc(task.title.lower())}">
  <header>
    <div>
      <span class="task-number">Task {task.number}</span>
      <h3>{esc(task.title)}</h3>
    </div>
    <div class="pill-row">
      {scope_badge}
      <span class="pill {esc(task.status_kind)}">{esc(task.status)}</span>
    </div>
  </header>
  <div class="progress" aria-label="{task.progress}% concluído"><span style="width:{task.progress}%"></span></div>
  <div class="meta-line">
    <span>{esc(task.mode or "modo não informado")}</span>
    <span>{esc(task.deadline or "prazo não informado")}</span>
    <span>{' · '.join(links) if links else 'sem links'}</span>
  </div>
  {detail}
</article>"""


def render_index(group_meta: dict[str, str], faculty_tasks: list[Task], stats: dict[str, int]) -> str:
    group_name = display_group_label(group_meta)
    project_name = display_project_label(group_meta)
    current_phase = next(
        (
            task.title
            for task in faculty_tasks
            if task.status_kind in {"warning", "danger"}
        ),
        "Sem task da disciplina em atenção",
    )
    body = f"""
{nav("index")}
<section class="hero hero-split">
  <div class="hero-copy">
    <span class="eyebrow">Painel central · {esc(project_name)}</span>
    <h1>Encontre rapidamente onde estamos e o que fazer agora.</h1>
    <p>Entrada visual do repositório: status das <strong>tasks da disciplina</strong>, próximos passos, onboarding e atalhos. Tasks de desenvolvimento do workflow ficam separadas no registry.</p>
    <div class="actions">
      <a class="button primary" href="grupo.html">Ver painel do grupo</a>
      <a class="button" href="registry.html">Ver registry visual</a>
      <a class="button" href="../../docs/workflows/00-onboarding-colega.md">Onboarding</a>
    </div>
  </div>
  <aside class="glass-card focus-card">
    <span>Fase atual</span>
    <strong>{esc(current_phase)}</strong>
    <p>Atualize o registry e rode o gerador para refrescar estes painéis.</p>
  </aside>
</section>
<section class="metrics-grid">
  {render_metric("tasks da disciplina", stats["tasks"])}
  {render_metric("em atenção", stats["active"])}
  {render_metric("pendências abertas", stats["pending"])}
  {render_metric("membros no grupo", stats["members"], hint=group_name)}
</section>
<section class="grid two">
  <div class="panel">
    <h2>Jornada do aluno</h2>
    <ol class="steps">
      <li><strong>Clonar e configurar:</strong> rode <code>python setup.py</code> e crie seu <code>LOCAL.md</code>.</li>
      <li><strong>Entender o grupo:</strong> abra <code>GROUP.md</code> e veja responsabilidades.</li>
      <li><strong>Ver status:</strong> use <code>grupo.html</code> e <code>registry.html</code>.</li>
      <li><strong>Executar task:</strong> siga o fluxo portal-first antes de implementar.</li>
      <li><strong>Estudar e defender:</strong> gere study packs quando a task exigir prova, vídeo ou apresentação.</li>
    </ol>
  </div>
  <div class="panel">
    <h2>Comandos úteis</h2>
    <pre><code>python scripts/update_workflow_dashboard.py
python setup.py
bash scripts/setup_fiap_automation.sh</code></pre>
    <p class="muted">Os HTMLs não são tempo real; eles são snapshots regeneráveis e versionáveis.</p>
  </div>
</section>
"""
    return html_page("Painel central — FIAP Workflow", body)


def render_group(
    group_meta: dict[str, str],
    members: list[Member],
    faculty_tasks: list[Task],
    stats: dict[str, int],
) -> str:
    group_name = display_group_label(group_meta)
    course = group_meta.get("Disciplina / módulo", "Disciplina não informada")
    task_cards = "\n".join(render_task_card(task, compact=True) for task in latest_tasks(faculty_tasks))
    member_cards = "\n".join(
        f"""<article class="member-card">
  <strong>{esc(member.name)}</strong>
  <span>{esc(member.rm)}</span>
  <p>{esc(member.responsibility)}</p>
</article>"""
        for member in members
    )
    pending_items = [item for task in latest_tasks(faculty_tasks) for item in task.pending[:2]][:8]
    pending_html = "".join(f"<li>{inline_md(item)}</li>" for item in pending_items)
    body = f"""
{nav("grupo")}
<section class="hero hero-split">
  <div class="hero-copy">
    <span class="eyebrow">{esc(course)}</span>
    <h1>{esc(group_name)}: visão do todo.</h1>
    <p>Resumo compartilhável para o WhatsApp do grupo: progresso das entregas da disciplina, pendências humanas e principais atalhos. Infra do repositório não entra neste painel.</p>
    <div class="actions">
      <a class="button primary" href="registry.html">Abrir registry visual</a>
      <a class="button" href="individual.html">Ver visão individual</a>
      <a class="button" href="../../GROUP.md">GROUP.md</a>
    </div>
  </div>
  <aside class="glass-card focus-card">
    <span>Próximo foco</span>
    <strong>Submissões e revisão final</strong>
    <p>As ações no portal FIAP continuam manuais.</p>
  </aside>
</section>
<section class="metrics-grid">
  {render_metric("tasks da disciplina", stats["tasks"])}
  {render_metric("prontas/históricas", stats["ready"])}
  {render_metric("ativas/atenção", stats["active"])}
  {render_metric("PDFs capturados", stats["pdfs"])}
</section>
<section class="grid main-aside">
  <div class="panel">
    <h2>Entregas em destaque</h2>
    <div class="stack">{task_cards}</div>
  </div>
  <aside class="panel">
    <h2>Próximas ações</h2>
    <ul class="checklist">{pending_html or '<li>Sem pendências abertas extraídas do registry.</li>'}</ul>
  </aside>
</section>
<section class="panel">
  <h2>Membros e responsabilidades</h2>
  <div class="member-grid">{member_cards}</div>
</section>
<section class="metrics-grid compact">
  {render_metric("workflows", stats["workflows"])}
  {render_metric("templates", stats["templates"])}
  {render_metric("scripts Python", stats["scripts"])}
  {render_metric("bases knowledge", stats["knowledge"])}
</section>
"""
    return html_page(f"{group_name} — Dashboard FIAP", body)


def member_payload(member: Member, faculty_tasks: list[Task]) -> dict[str, object]:
    normalized = normalize(member.name)
    is_po = "product owner" in normalize(member.responsibility) or "higor" in normalized
    related = latest_tasks(faculty_tasks) if is_po else [
        task for task in latest_tasks(faculty_tasks) if "GRUPO" in task.mode.upper()
    ][:4]
    if not related:
        related = latest_tasks(faculty_tasks)[:3]
    focus = [
        {
            "title": f"Task {task.number}: {task.title}",
            "text": task.pending[0] if task.pending else task.status,
            "kind": task.status_kind,
        }
        for task in related
    ]
    checklist = [
        "Rodar `python setup.py` para criar LOCAL.md.",
        "Conferir sua linha em GROUP.md.",
        "Abrir o painel do grupo antes de começar.",
        "Usar o fluxo portal-first para task nova.",
    ]
    if is_po:
        checklist.extend([
            "Revisar checklist de segurança antes do push.",
            "Integrar partes do grupo e registrar pendências humanas.",
        ])
    else:
        checklist.extend([
            "Pedir à IA somente sua parte quando existir SPLIT.md.",
            "Enviar evidências para integração final.",
        ])
    return {
        "name": member.name,
        "rm": member.rm,
        "role": member.responsibility,
        "tasks": len(related),
        "pending": sum(len(task.pending) for task in related),
        "artifacts": sum(1 for task in related if task.folder or task.spec),
        "focus": focus,
        "checklist": checklist,
    }


def render_individual(members: list[Member], faculty_tasks: list[Task]) -> str:
    data = {slug(member.name): member_payload(member, faculty_tasks) for member in members}
    first_key = next(
        (slug(member.name) for member in members if "product owner" in normalize(member.responsibility)),
        next(iter(data), ""),
    )
    options = "".join(f'<option value="{esc(key)}">{esc(value["name"])}</option>' for key, value in data.items())
    body = f"""
{nav("individual")}
<section class="hero hero-split">
  <div class="hero-copy">
    <span class="eyebrow">Visão individual</span>
    <h1 id="personTitle">Meu recorte do workflow.</h1>
    <p id="personSubtitle">Escolha um integrante para ver foco, pendências e próximos passos sem depender de <code>LOCAL.md</code> commitado.</p>
    <div class="metrics-grid inline">
      <article class="metric"><strong id="metricTasks">0</strong><span>tarefas relacionadas</span></article>
      <article class="metric"><strong id="metricPending">0</strong><span>pendências</span></article>
      <article class="metric"><strong id="metricArtifacts">0</strong><span>artefatos úteis</span></article>
    </div>
  </div>
  <aside class="glass-card focus-card">
    <label for="memberSelect">Integrante</label>
    <select id="memberSelect">{options}</select>
    <strong id="memberName"></strong>
    <p id="memberRole"></p>
  </aside>
</section>
<section class="grid main-aside">
  <div class="panel">
    <h2>O que olhar agora</h2>
    <div id="focusCards" class="stack"></div>
  </div>
  <aside class="panel">
    <h2>Checklist pessoal</h2>
    <ul id="personalChecklist" class="checklist"></ul>
  </aside>
</section>
<section class="panel">
  <h2>Prompts rápidos</h2>
  <div class="prompt-grid">
    <pre><code>Quero fazer apenas minha parte.
Leia GROUP.md, LOCAL.md e specs/&lt;task&gt;/SPLIT.md.</code></pre>
    <pre><code>Leia SPEC.md, WORKPLAN.md, REVIEW.md e liste riscos antes da entrega.</code></pre>
  </div>
</section>
<script>
const members = {json.dumps(data, ensure_ascii=False)};
const initialMember = {json.dumps(first_key, ensure_ascii=False)};
const select = document.querySelector("#memberSelect");
function escapeHtml(value) {{
  return String(value).replace(/[&<>"']/g, (char) => ({{"&":"&amp;","<":"&lt;",">":"&gt;","\\\"":"&quot;","'":"&#39;"}}[char]));
}}
function render(key) {{
  const item = members[key] || members[initialMember];
  document.querySelector("#personTitle").textContent = item.name + ": visão de trabalho";
  document.querySelector("#memberName").textContent = item.name + " · " + item.rm;
  document.querySelector("#memberRole").textContent = item.role;
  document.querySelector("#metricTasks").textContent = item.tasks;
  document.querySelector("#metricPending").textContent = item.pending;
  document.querySelector("#metricArtifacts").textContent = item.artifacts;
  document.querySelector("#focusCards").innerHTML = item.focus.map((card) => `
    <article class="task-card">
      <header><div><h3>${{escapeHtml(card.title)}}</h3></div><span class="pill ${{card.kind}}">${{card.kind}}</span></header>
      <p class="muted">${{escapeHtml(card.text)}}</p>
    </article>
  `).join("");
  document.querySelector("#personalChecklist").innerHTML = item.checklist.map((text) => `<li>${{escapeHtml(text)}}</li>`).join("");
}}
select.addEventListener("change", () => render(select.value));
select.value = initialMember;
render(initialMember);
</script>
"""
    return html_page("Visão individual — FIAP Workflow", body)


def render_registry(
    faculty_tasks: list[Task],
    workflow_tasks: list[Task],
    stats: dict[str, int],
) -> str:
    faculty_cards = "\n".join(render_task_card(task) for task in faculty_tasks)
    workflow_cards = "\n".join(render_task_card(task) for task in workflow_tasks)
    workflow_section = ""
    if workflow_cards:
        workflow_section = f"""
<section class="panel workflow-panel">
  <h2>Desenvolvimento do workflow</h2>
  <p class="muted">Tasks de infraestrutura do repositório — não são entregas da disciplina e não entram nas métricas do grupo.</p>
  <div class="stack">{workflow_cards}</div>
</section>
"""
    body = f"""
{nav("registry")}
<section class="hero">
  <div class="hero-copy">
    <span class="eyebrow">Task Registry visual</span>
    <h1>Mapa navegável das tasks da disciplina.</h1>
    <p>Visão HTML do <code>TASK_REGISTRY.md</code>: entregas FIAP em destaque; desenvolvimento do repositório fica separado abaixo.</p>
    <div class="actions">
      <a class="button primary" href="../../TASK_REGISTRY.md">Abrir Markdown original</a>
      <a class="button" href="grupo.html">Ver grupo</a>
    </div>
  </div>
</section>
<section class="metrics-grid">
  {render_metric("tasks da disciplina", stats["tasks"])}
  {render_metric("prontas/históricas", stats["ready"])}
  {render_metric("ativas/atenção", stats["active"])}
  {render_metric("infra workflow", stats["workflow_tasks"])}
</section>
<section class="panel">
  <div class="toolbar">
    <input id="search" type="search" placeholder="Buscar por task, status, disciplina...">
    <button data-filter="all" class="filter active">Todas (disciplina)</button>
    <button data-filter="warning" class="filter">Em andamento</button>
    <button data-filter="danger" class="filter">Atenção</button>
    <button data-filter="success" class="filter">Prontas</button>
  </div>
  <div id="taskList" class="stack">{faculty_cards}</div>
</section>
{workflow_section}
<script>
const search = document.querySelector("#search");
const buttons = [...document.querySelectorAll(".filter")];
const cards = [...document.querySelectorAll("#taskList .task-card")];
let currentFilter = "all";
function applyFilters() {{
  const query = search.value.trim().toLowerCase();
  cards.forEach((card) => {{
    const matchesFilter = currentFilter === "all" || card.dataset.kind === currentFilter;
    const matchesQuery = !query || card.textContent.toLowerCase().includes(query);
    card.hidden = !(matchesFilter && matchesQuery);
  }});
}}
buttons.forEach((button) => button.addEventListener("click", () => {{
  currentFilter = button.dataset.filter;
  buttons.forEach((item) => item.classList.toggle("active", item === button));
  applyFilters();
}}));
search.addEventListener("input", applyFilters);
</script>
"""
    return html_page("Task Registry visual — FIAP Workflow", body)


STYLE = """
<style>
:root {
  --bg: #0f172a;
  --panel: rgba(15, 23, 42, 0.78);
  --card: rgba(255,255,255,0.08);
  --text: #e5eefb;
  --muted: #94a3b8;
  --line: rgba(148,163,184,0.22);
  --blue: #38bdf8;
  --purple: #a78bfa;
  --green: #22c55e;
  --yellow: #f59e0b;
  --red: #fb7185;
  --dark: #0f172a;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  color: var(--text);
  background:
    radial-gradient(circle at top left, rgba(56,189,248,0.22), transparent 28rem),
    radial-gradient(circle at 90% 10%, rgba(167,139,250,0.22), transparent 30rem),
    linear-gradient(135deg, #020617 0%, #0f172a 55%, #111827 100%);
}
a { color: inherit; }
code, pre { font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace; }
pre {
  overflow: auto;
  margin: 0;
  padding: 16px;
  border-radius: 18px;
  background: rgba(15,23,42,0.92);
  color: #e2e8f0;
}
.shell { width: min(1180px, calc(100% - 32px)); margin: 0 auto; padding: 24px 0 44px; }
.topbar { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 18px; }
.navlink, .button {
  display: inline-flex;
  align-items: center;
  min-height: 40px;
  padding: 0 14px;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: rgba(255,255,255,0.08);
  text-decoration: none;
  font-weight: 800;
}
.navlink.active, .button.primary {
  border-color: transparent;
  background: linear-gradient(135deg, var(--blue), var(--purple));
  color: #020617;
}
.hero {
  margin-bottom: 18px;
  padding: 30px;
  border: 1px solid var(--line);
  border-radius: 30px;
  background: var(--panel);
  box-shadow: 0 24px 80px rgba(2,6,23,0.24);
  backdrop-filter: blur(18px);
}
.hero-split { display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.65fr); gap: 20px; }
.eyebrow {
  display: inline-block;
  margin-bottom: 14px;
  color: var(--blue);
  font-size: .78rem;
  font-weight: 900;
  letter-spacing: .09em;
  text-transform: uppercase;
}
h1, h2, h3, p { margin-top: 0; }
h1 { max-width: 850px; margin-bottom: 14px; font-size: clamp(2.15rem, 6vw, 4.8rem); line-height: .96; letter-spacing: -.06em; }
h2 { margin-bottom: 16px; font-size: 1.35rem; letter-spacing: -.035em; }
h3 { margin-bottom: 8px; letter-spacing: -.02em; }
p { color: var(--muted); line-height: 1.65; }
.actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 22px; }
.glass-card, .panel, .metric, .task-card, .member-card {
  border: 1px solid var(--line);
  border-radius: 24px;
  background: var(--panel);
  box-shadow: 0 16px 48px rgba(2,6,23,0.12);
}
.panel { padding: 24px; }
.focus-card { padding: 22px; align-self: stretch; }
.focus-card span, .metric span, .task-number {
  color: var(--muted);
  font-size: .76rem;
  font-weight: 900;
  letter-spacing: .08em;
  text-transform: uppercase;
}
.focus-card strong { display: block; margin: 10px 0; font-size: 1.8rem; line-height: 1.05; letter-spacing: -.05em; }
.metrics-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin-bottom: 18px; }
.metrics-grid.inline { grid-template-columns: repeat(3, minmax(0, 1fr)); margin: 18px 0 0; }
.metrics-grid.compact { margin-top: 18px; }
.metric { padding: 18px; background: var(--card); }
.metric strong { display: block; font-size: 2.1rem; letter-spacing: -.05em; }
.metric small { display: block; margin-top: 6px; color: var(--muted); }
.grid { display: grid; gap: 18px; margin-bottom: 18px; }
.grid.two, .grid.main-aside { grid-template-columns: minmax(0, 1.35fr) minmax(280px, .65fr); }
.stack { display: grid; gap: 12px; }
.task-card { padding: 18px; background: var(--card); }
.task-card[hidden] { display: none; }
.task-card header { display: flex; align-items: flex-start; justify-content: space-between; gap: 14px; }
.pill-row { display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-end; }
.scope-pill { opacity: 0.92; }
.workflow-panel { margin-top: 18px; border-style: dashed; }
.pill {
  display: inline-flex;
  flex-shrink: 0;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: .72rem;
  font-weight: 900;
  text-transform: uppercase;
}
.pill.success { color: #bbf7d0; background: rgba(34,197,94,.18); }
.pill.warning { color: #fde68a; background: rgba(245,158,11,.18); }
.pill.danger { color: #fecdd3; background: rgba(251,113,133,.18); }
.pill.info { color: #bae6fd; background: rgba(56,189,248,.18); }
.progress { overflow: hidden; height: 9px; margin: 14px 0; border-radius: 999px; background: rgba(148,163,184,.2); }
.progress span { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, var(--blue), var(--green)); }
.meta-line { display: flex; flex-wrap: wrap; gap: 12px; color: var(--muted); font-size: .86rem; }
.card-detail { margin-top: 14px; }
.card-detail ul, .checklist { margin: 0; padding-left: 18px; color: var(--muted); line-height: 1.6; }
.member-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
.member-card { padding: 16px; background: var(--card); }
.member-card strong { display: block; margin-bottom: 4px; }
.member-card span, .muted { color: var(--muted); }
.steps { margin: 0; padding-left: 22px; color: var(--muted); line-height: 1.75; }
.toolbar { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; }
.toolbar input, select {
  min-height: 42px;
  padding: 0 14px;
  border: 1px solid var(--line);
  border-radius: 14px;
  background: rgba(15,23,42,0.55);
  color: var(--text);
  font: inherit;
}
.toolbar input::placeholder { color: var(--muted); }
.toolbar input { flex: 1 1 260px; }
.filter { min-height: 42px; padding: 0 13px; border: 1px solid var(--line); border-radius: 999px; background: rgba(255,255,255,0.08); color: var(--text); font-weight: 800; cursor: pointer; }
.filter.active { background: linear-gradient(135deg, var(--blue), var(--purple)); color: #020617; border-color: transparent; }
.prompt-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.footer { margin-top: 20px; color: var(--muted); text-align: center; font-size: .88rem; }
@media (max-width: 900px) {
  .hero-split, .grid.two, .grid.main-aside, .prompt-grid { grid-template-columns: 1fr; }
  .metrics-grid, .metrics-grid.inline, .member-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 560px) {
  .shell { width: min(100% - 20px, 1180px); padding-top: 12px; }
  .hero, .panel { padding: 18px; border-radius: 22px; }
  .metrics-grid, .metrics-grid.inline, .member-grid { grid-template-columns: 1fr; }
  .task-card header { display: block; }
  .pill { margin-top: 8px; }
}
</style>
"""


def write(path: Path, content: str, check: bool = False) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    if check:
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def source_signature(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()[:12]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Atualiza dashboards HTML do workflow FIAP.")
    parser.add_argument("--registry", default=str(REGISTRY_PATH), help="Caminho do TASK_REGISTRY.md.")
    parser.add_argument("--group", default=str(GROUP_PATH), help="Caminho do GROUP.md.")
    parser.add_argument("--out", default=str(DASHBOARD_DIR), help="Pasta de saída dos HTMLs.")
    parser.add_argument("--quiet", action="store_true", help="Não imprime saída quando a execução termina com sucesso.")
    parser.add_argument("--check", action="store_true", help="Verifica se os dashboards estão atualizados sem escrever arquivos.")
    return parser.parse_args()


def main() -> None:
    global SOURCE_SIGNATURE
    args = parse_args()
    registry_path = Path(args.registry)
    group_path = Path(args.group)
    out_dir = Path(args.out)
    SOURCE_SIGNATURE = source_signature([registry_path, group_path])
    registry_text = registry_path.read_text(encoding="utf-8")
    group_text = group_path.read_text(encoding="utf-8")
    tasks = parse_tasks(registry_text)
    faculty_tasks, workflow_tasks = split_tasks(tasks)
    group_meta, members = parse_group(group_text)
    stats = collect_stats(faculty_tasks, workflow_tasks, members, registry_text)

    pages = {
        "index.html": render_index(group_meta, faculty_tasks, stats),
        "grupo.html": render_group(group_meta, members, faculty_tasks, stats),
        "individual.html": render_individual(members, faculty_tasks),
        "registry.html": render_registry(faculty_tasks, workflow_tasks, stats),
    }
    changed = [name for name, content in pages.items() if write(out_dir / name, content, check=args.check)]
    if args.check and changed:
        if not args.quiet:
            print("Dashboards desatualizados:")
            for name in changed:
                print(f"- {name}")
        raise SystemExit(1)
    if not args.quiet:
        if changed:
            print(f"Dashboards atualizados em {out_dir}")
            for name in changed:
                print(f"- {name}")
        else:
            print("Dashboards já estavam atualizados.")


if __name__ == "__main__":
    main()
