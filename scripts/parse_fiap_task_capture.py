#!/usr/bin/env python3
"""
Parser para transformar captura bruta da FIAP em estrutura reutilizavel.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import List, Optional


SECTION_MARKERS = {
    "[METADADOS]",
    "[TEXTO PRINCIPAL]",
    "[DISCLAIMERS E AVISOS]",
    "[IMAGENS]",
    "[LINKS/ANEXOS]",
}


@dataclass
class ChapterItem:
    capitulo: str
    progresso: Optional[str] = None
    atividade: Optional[str] = None


@dataclass
class ParsedCapture:
    url: str = ""
    disciplina_fase_cap: str = ""
    data_hora: str = ""
    fase_titulo: str = ""
    janela: str = ""
    objetivo: str = ""
    capitulo_foco: str = ""
    capitulos: List[ChapterItem] = field(default_factory=list)
    disclaimers: List[str] = field(default_factory=list)
    imagens: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)


def _extract_between(text: str, start: str, end: Optional[str] = None) -> str:
    start_idx = text.find(start)
    if start_idx < 0:
        return ""
    start_idx += len(start)
    if end is None:
        return text[start_idx:].strip()
    end_idx = text.find(end, start_idx)
    if end_idx < 0:
        return text[start_idx:].strip()
    return text[start_idx:end_idx].strip()


def _extract_payload(text: str) -> str:
    fence = re.search(r"```markdown\s*(.*?)```", text, flags=re.S | re.I)
    return fence.group(1).strip() if fence else text


def _clean_lines(block: str) -> List[str]:
    return [line.strip() for line in block.splitlines() if line.strip()]


def parse_capture(text: str) -> ParsedCapture:
    payload = _extract_payload(text)
    metadata_block = _extract_between(payload, "[METADADOS]", "[TEXTO PRINCIPAL]")
    principal_block = _extract_between(payload, "[TEXTO PRINCIPAL]", "[DISCLAIMERS E AVISOS]")
    disclaimers_block = _extract_between(payload, "[DISCLAIMERS E AVISOS]", "[IMAGENS]")
    images_block = _extract_between(payload, "[IMAGENS]", "[LINKS/ANEXOS]")
    links_block = _extract_between(payload, "[LINKS/ANEXOS]")

    parsed = ParsedCapture()

    for line in _clean_lines(metadata_block):
        if line.startswith("URL:"):
            parsed.url = line.replace("URL:", "", 1).strip()
        elif line.startswith("Disciplina/Fase/Cap:"):
            parsed.disciplina_fase_cap = line.replace("Disciplina/Fase/Cap:", "", 1).strip()
        elif line.startswith("Data/Hora da cópia:"):
            parsed.data_hora = line.replace("Data/Hora da cópia:", "", 1).strip()

    main_lines = _clean_lines(principal_block)
    for i, line in enumerate(main_lines):
        if re.match(r"^Fase\s+\d+\s+-\s+", line):
            parsed.fase_titulo = line
        elif re.match(r"^de\s+\d{2}/\d{2}/\d{4}\s+até\s+\d{2}/\d{2}/\d{4}$", line):
            parsed.janela = line
        elif line.startswith("Objetivo:"):
            parsed.objetivo = line.replace("Objetivo:", "", 1).strip()
        elif re.match(r"^Cap\s+\d+\s+-\s+", line) and not parsed.capitulo_foco:
            parsed.capitulo_foco = line

        if line == "Capítulos":
            _parse_chapters(main_lines, i + 1, parsed)
            break

    parsed.disclaimers = _extract_list_block(disclaimers_block)
    parsed.imagens = _extract_list_block(images_block)
    parsed.links = _extract_list_block(links_block)

    return parsed


def _parse_chapters(lines: List[str], start_idx: int, parsed: ParsedCapture) -> None:
    chapter_indexes = [i for i in range(start_idx, len(lines)) if re.match(r"^Cap\s+\d+\s+-\s+", lines[i])]

    for pos, cap_idx in enumerate(chapter_indexes):
        cap_title = lines[cap_idx]
        next_cap_idx = chapter_indexes[pos + 1] if pos + 1 < len(chapter_indexes) else len(lines)
        window = lines[cap_idx + 1 : next_cap_idx]

        progress = next((x for x in window if re.search(r"\d+%", x)), None)
        activity = next((x for x in window if x.lower().startswith("fast test") or x.lower().startswith("how to")), None)

        parsed.capitulos.append(
            ChapterItem(
                capitulo=cap_title,
                progresso=progress,
                atividade=activity,
            )
        )


def _extract_list_block(block: str) -> List[str]:
    result = []
    for line in _clean_lines(block):
        if line in SECTION_MARKERS:
            continue
        if line.startswith("- "):
            result.append(line[2:].strip())
        elif not line.startswith("("):
            result.append(line)
    return result


def to_markdown(parsed: ParsedCapture) -> str:
    lines = [
        "# Snapshot Estruturado — Página de Task FIAP",
        "",
        "## Metadados",
        f"- URL: {parsed.url or 'N/D'}",
        f"- Disciplina/Fase/Cap: {parsed.disciplina_fase_cap or 'N/D'}",
        f"- Data/Hora da cópia: {parsed.data_hora or 'N/D'}",
        "",
        "## Resumo da Fase",
        f"- Título da fase: {parsed.fase_titulo or 'N/D'}",
        f"- Janela: {parsed.janela or 'N/D'}",
        f"- Objetivo: {parsed.objetivo or 'N/D'}",
        f"- Capítulo foco da captura: {parsed.capitulo_foco or 'N/D'}",
        "",
        "## Capítulos detectados",
    ]

    if not parsed.capitulos:
        lines.append("- Nenhum capítulo detectado.")
    else:
        for item in parsed.capitulos:
            lines.append(
                f"- {item.capitulo} | progresso: {item.progresso or 'N/D'} | atividade: {item.atividade or 'N/D'}"
            )

    lines.append("")
    lines.append("## Disclaimers e avisos")
    lines.extend([f"- {x}" for x in parsed.disclaimers] or ["- N/D"])

    lines.append("")
    lines.append("## Imagens")
    lines.extend([f"- {x}" for x in parsed.imagens] or ["- N/D"])

    lines.append("")
    lines.append("## Links/Anexos")
    lines.extend([f"- {x}" for x in parsed.links] or ["- N/D"])

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Parseia captura de task FIAP em JSON e Markdown.")
    parser.add_argument("input_file", help="Arquivo markdown com captura preenchida")
    parser.add_argument(
        "--json-out",
        default="docs/validation/fiap_capture_parsed.json",
        help="Caminho do JSON de saida",
    )
    parser.add_argument(
        "--md-out",
        default="docs/validation/fiap_capture_parsed.md",
        help="Caminho do Markdown estruturado de saida",
    )
    args = parser.parse_args()

    source = Path(args.input_file)
    payload = source.read_text(encoding="utf-8")
    parsed = parse_capture(payload)

    json_out = Path(args.json_out)
    md_out = Path(args.md_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)

    json_out.write_text(json.dumps(asdict(parsed), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_out.write_text(to_markdown(parsed), encoding="utf-8")

    print(f"JSON salvo em: {json_out}")
    print(f"Markdown salvo em: {md_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
