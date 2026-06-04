#!/usr/bin/env python3
"""Setup interativo do Framework FIAP.

Sem dependencias externas. Gera LOCAL.md, opcionalmente atualiza GROUP.md e
orienta os proximos passos Git sem fazer push ou gravar credenciais.
"""

from __future__ import annotations

import argparse
import os
import platform
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent


@dataclass
class Student:
    name: str
    rm: str
    email: str
    github: str
    ide: str
    branch: str
    current_focus: str


@dataclass
class Group:
    mode: str
    discipline: str
    class_code: str
    group_name: str
    project_name: str
    repo_url: str
    branch_convention: str
    members: list[tuple[str, str, str, str]]


def run_command(args: list[str]) -> str:
    try:
        return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def detect_environment() -> dict[str, str]:
    return {
        "os": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
        "git": run_command(["git", "--version"]) or "nao encontrado",
        "branch": run_command(["git", "branch", "--show-current"]) or "sem branch",
        "remote": run_command(["git", "remote", "get-url", "origin"]) or "sem remote origin",
        "cwd": str(ROOT),
    }


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def ask_yes_no(prompt: str, default: bool = False) -> bool:
    default_label = "s" if default else "n"
    value = ask(f"{prompt} (s/n)", default_label).lower()
    return value in {"s", "sim", "y", "yes"}


def slugify(value: str) -> str:
    clean = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    clean = "-".join(part for part in clean.split("-") if part)
    return clean or "aluno"


def collect_student(env: dict[str, str], non_interactive: bool) -> Student:
    if non_interactive:
        return Student(
            name="Aluno Exemplo",
            rm="",
            email="",
            github="@aluno",
            ide="VS Code / Copilot",
            branch="parte1-aluno-exemplo",
            current_focus="Configurar o framework e validar o fluxo.",
        )

    name = ask("Seu nome (como a IA deve te chamar)")
    rm = ask("RM (opcional)")
    email = ask("Email institucional (opcional, sem senha)")
    github = ask("GitHub (@usuario ou URL, opcional)")
    ide = ask("IDE principal", "Cursor / VS Code / Claude Code / Antigravity")
    suggested_branch = f"parte1-{slugify(name)}" if name else env["branch"]
    branch = ask("Branch sugerida para seu trabalho", suggested_branch)
    current_focus = ask("O que voce esta fazendo agora?", "Configurar o framework")
    return Student(name, rm, email, github, ide, branch, current_focus)


def collect_group(non_interactive: bool) -> Group:
    if non_interactive:
        return Group(
            mode="grupo",
            discipline="Disciplina Exemplo",
            class_code="",
            group_name="Grupo Exemplo",
            project_name="Projeto Exemplo",
            repo_url="https://github.com/exemplo/repo",
            branch_convention="parteN-nome",
            members=[
                ("Aluno Exemplo", "", "@aluno", "Parte 1"),
                ("Colega Exemplo", "", "@colega", "Parte 2"),
            ],
        )

    mode = ask("Uso principal (solo/grupo)", "grupo").lower()
    discipline = ask("Disciplina / modulo", "A definir")
    class_code = ask("Turma / codigo (opcional)")
    group_name = ask("Nome ou numero do grupo", "Grupo a definir")
    project_name = ask("Nome curto do projeto (opcional)")
    repo_url = ask("URL do repositorio de entrega (opcional)")
    branch_convention = ask("Convencao de branches", "parteN-nome")

    members: list[tuple[str, str, str, str]] = []
    if mode == "grupo":
        print("\nCadastre membros. Deixe o nome vazio para terminar.")
        while True:
            name = ask("Nome do membro")
            if not name:
                break
            rm = ask("RM (opcional)")
            github = ask("GitHub (opcional)")
            responsibility = ask("Responsabilidade inicial", "A definir")
            members.append((name, rm, github, responsibility))

    return Group(mode, discipline, class_code, group_name, project_name, repo_url, branch_convention, members)


def write_local(student: Student) -> None:
    content = f"""# Identificacao local (este clone / esta maquina)

> Este arquivo e local e nao deve ser commitado. Ele identifica quem esta usando a IA neste clone.

## Quem esta usando o assistente aqui

- **Nome:** {student.name}
- **RM:** {student.rm or "_nao informado_"}
- **Email institucional:** {student.email or "_nao informado_"}
- **GitHub:** {student.github or "_nao informado_"}
- **IDE principal:** {student.ide}

## Notas locais

- **Branch habitual:** {student.branch}
- **Foco atual:** {student.current_focus}
"""
    (ROOT / "LOCAL.md").write_text(content, encoding="utf-8")


def render_group(group: Group, existing_note: str = "") -> str:
    rows = "\n".join(
        f"| {name} | {rm} | {github} | {responsibility} |"
        for name, rm, github, responsibility in group.members
    )
    if not rows:
        rows = "| _(preencher)_ | | | |"

    return f"""# Identificacao do grupo

> Preencher pelo grupo e manter atualizado no Git para todos compartilharem o mesmo contexto.
{existing_note}
## Disciplina e turma

- **Disciplina / modulo:** {group.discipline}
- **Turma / codigo da turma:** {group.class_code or "_opcional_"}

## Grupo

- **Nome ou numero do grupo:** {group.group_name}
- **Nome curto do projeto (opcional):** {group.project_name or "_opcional_"}
- **Link do repositorio de entrega (GitHub):** {group.repo_url or "_a definir_"}

## Membros

| Nome | RM | GitHub (@ ou URL) | Responsabilidade / partes do trabalho |
|------|----|-------------------|----------------------------------------|
{rows}

## Notas para a IA

- **Modo principal:** {group.mode}
- **Convencao de branches:** {group.branch_convention}
- **Canal de comunicacao do grupo:** _preencher se fizer sentido, sem credenciais_
"""


def maybe_update_group(group: Group, non_interactive: bool) -> None:
    group_path = ROOT / "GROUP.md"
    if non_interactive:
        target = ROOT / "GROUP.generated.example.md"
        target.write_text(render_group(group, "\n> Exemplo gerado por `python setup.py --non-interactive`.\n"), encoding="utf-8")
        return

    if ask_yes_no("Atualizar GROUP.md com essas informacoes?", default=False):
        group_path.write_text(render_group(group), encoding="utf-8")
        print("GROUP.md atualizado. Revise antes de commitar.")
    else:
        print("GROUP.md nao foi alterado.")


def print_next_steps(student: Student, group: Group, env: dict[str, str]) -> None:
    print("\nSetup concluido.")
    print("\nAmbiente detectado:")
    for key, value in env.items():
        print(f"- {key}: {value}")

    print("\nProximos passos recomendados:")
    print("1. Abra README.md, SETUP.md e docs/FRAMEWORK.md no seu IDE.")
    print("2. Revise LOCAL.md (local) e GROUP.md (grupo).")
    print("3. Para task nova: cole o enunciado no chat e peca o fluxo spec-driven.")
    print("4. Para aula nova: anexe o PDF ou cole o texto da pagina e peca ingestao em knowledge/.")

    print("\nPrompts prontos:")
    print("- Task: 'Vou colar uma task da FIAP. Extraia requisitos, pergunte solo/grupo e crie SPEC.md antes de executar.'")
    print("- Aula: 'Vou enviar uma aula por PDF/texto copiado. Gere pilula em knowledge/ e atualize flashcards.md.'")
    print("- Grupo: 'Quero fazer apenas minha parte. Use GROUP.md, LOCAL.md e SPLIT.md para limitar o escopo.'")

    if shutil.which("git"):
        print("\nGit sugerido para trabalho em grupo:")
        print("git checkout main")
        print("git pull origin main")
        print(f"git checkout -b {student.branch}")
        print("# trabalhe na sua parte, depois:")
        print("git status")
        print("git add <arquivos>")
        print('git commit -m "feat: entrega minha parte"')
        print(f"git push -u origin {student.branch}")

    if group.mode == "grupo":
        print("\nLembrete: PR deve citar a parte correspondente em specs/<task>/SPLIT.md.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Configura o Framework FIAP neste clone.")
    parser.add_argument("--non-interactive", action="store_true", help="Gera LOCAL.md e GROUP.generated.example.md com dados de exemplo.")
    args = parser.parse_args()

    env = detect_environment()
    print("Framework FIAP — setup interativo\n")
    student = collect_student(env, args.non_interactive)
    group = collect_group(args.non_interactive)
    write_local(student)
    maybe_update_group(group, args.non_interactive)
    print_next_steps(student, group, env)


if __name__ == "__main__":
    main()
