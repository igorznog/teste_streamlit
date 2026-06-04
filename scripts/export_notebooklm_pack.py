#!/usr/bin/env python3
"""Exporta fontes seguras para uso no NotebookLM.

O script copia Markdown/texto/CSV/JSON de `knowledge/` e `specs/` por padrao,
remove PII simples quando possivel e gera um indice de revisao manual.
"""

from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAFE_EXTENSIONS = {".md", ".txt", ".csv", ".json"}
PDF_EXTENSIONS = {".pdf"}
EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    ".agent-browser",
    "captures",
    "prints",
}
SECRET_NAMES = {
    ".env",
    "credentials.json",
    "cookies.json",
    "cookie.txt",
    "token.json",
}


@dataclass
class ExportedFile:
    source: Path
    target: Path
    warnings: list[str]


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def sanitize_text(text: str) -> tuple[str, list[str]]:
    warnings: list[str] = []
    patterns = [
        (re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"), "[EMAIL_REMOVIDO]", "email"),
        (re.compile(r"\bRM\s*:?\s*\d{4,8}\b", re.IGNORECASE), "RM [REMOVIDO]", "rm"),
        (re.compile(r"\b\d{6}\b"), "[NUMERO_6_DIGITOS_REMOVIDO]", "numero_6_digitos"),
        (re.compile(r"(password|senha|token|cookie)\s*[:=]\s*\S+", re.IGNORECASE), r"\1=[REMOVIDO]", "segredo"),
    ]
    sanitized = text
    for pattern, replacement, label in patterns:
        sanitized, count = pattern.subn(replacement, sanitized)
        if count:
            warnings.append(f"{label}: {count} ocorrencia(s) removida(s)")
    return sanitized, warnings


def should_skip(path: Path, include_pdf: bool, max_mb: float) -> str | None:
    if any(part in EXCLUDED_PARTS for part in path.parts):
        return "pasta excluida"
    if path.name in SECRET_NAMES:
        return "nome sensivel"
    if path.suffix.lower() in PDF_EXTENSIONS and not include_pdf:
        return "PDF desativado por padrao"
    if path.suffix.lower() not in SAFE_EXTENSIONS | (PDF_EXTENSIONS if include_pdf else set()):
        return "extensao nao suportada"
    if path.stat().st_size > max_mb * 1024 * 1024:
        return f"arquivo maior que {max_mb} MB"
    return None


def iter_files(sources: list[Path]) -> list[Path]:
    files: list[Path] = []
    for source in sources:
        if source.is_file():
            files.append(source)
        elif source.is_dir():
            files.extend(path for path in source.rglob("*") if path.is_file())
    return sorted(files)


def export_file(path: Path, source_root: Path, dest: Path, redact_pii: bool) -> ExportedFile:
    relative = path.relative_to(source_root)
    target = dest / source_root.name / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    warnings: list[str] = []

    if path.suffix.lower() in SAFE_EXTENSIONS:
        text = path.read_text(encoding="utf-8", errors="replace")
        if redact_pii:
            text, warnings = sanitize_text(text)
        target.write_text(text, encoding="utf-8")
    else:
        shutil.copy2(path, target)
        warnings.append("arquivo binario copiado sem inspecao")

    return ExportedFile(path, target, warnings)


def find_source_root(path: Path, sources: list[Path]) -> Path:
    matches = [source for source in sources if is_relative_to(path, source)]
    return max(matches, key=lambda item: len(item.parts))


def write_index(dest: Path, exported: list[ExportedFile], skipped: list[tuple[Path, str]]) -> None:
    lines = [
        "# NotebookLM Pack",
        "",
        f"Gerado em: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "## Como usar",
        "",
        "1. Revise este indice.",
        "2. Confirme se nao ha dados pessoais ou material restrito.",
        "3. Suba a pasta para Google Drive.",
        "4. Crie um notebook no NotebookLM e adicione as fontes.",
        "",
        "## Arquivos exportados",
        "",
    ]
    for item in exported:
        rel = item.target.relative_to(dest)
        lines.append(f"- `{rel}` <- `{item.source.relative_to(ROOT)}`")
        for warning in item.warnings:
            lines.append(f"  - Aviso: {warning}")

    lines.extend(["", "## Arquivos ignorados", ""])
    if skipped:
        for path, reason in skipped:
            display = path.relative_to(ROOT) if is_relative_to(path, ROOT) else path
            lines.append(f"- `{display}`: {reason}")
    else:
        lines.append("- Nenhum.")

    lines.extend(
        [
            "",
            "## Checklist manual",
            "",
            "- [ ] Fontes conferidas.",
            "- [ ] PII removida ou justificada.",
            "- [ ] PDFs/capturas restritas nao publicados indevidamente.",
            "- [ ] NotebookLM criado com as fontes certas.",
        ]
    )
    (dest / "00_INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Exporta pacote seguro para NotebookLM.")
    parser.add_argument("--source", action="append", default=[], help="Arquivo ou pasta fonte. Pode repetir.")
    parser.add_argument("--dest", default=str(Path.home() / "FIAP_NotebookLM"), help="Pasta destino.")
    parser.add_argument("--include-pdf", action="store_true", help="Inclui PDFs. Revise copyright antes de compartilhar.")
    parser.add_argument("--no-redact-pii", action="store_true", help="Nao remove PII simples dos textos.")
    parser.add_argument("--max-mb", type=float, default=8.0, help="Tamanho maximo por arquivo.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    sources = [ROOT / source for source in args.source] if args.source else [ROOT / "knowledge", ROOT / "specs"]
    sources = [source.resolve() for source in sources if source.exists()]
    if not sources:
        raise SystemExit("Nenhuma fonte encontrada.")

    dest = Path(args.dest).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)

    exported: list[ExportedFile] = []
    skipped: list[tuple[Path, str]] = []
    files = iter_files(sources)
    for path in files:
        reason = should_skip(path, args.include_pdf, args.max_mb)
        if reason:
            skipped.append((path, reason))
            continue
        source_root = find_source_root(path, sources)
        exported.append(export_file(path, source_root, dest, redact_pii=not args.no_redact_pii))

    write_index(dest, exported, skipped)
    print(f"Exportados {len(exported)} arquivos para {dest}")
    print(f"Indice: {dest / '00_INDEX.md'}")


if __name__ == "__main__":
    main()
