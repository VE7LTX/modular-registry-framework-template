from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from modular_registry_framework.modules.workspace_scanner.service import SKIP_DIRS


SECRET_PATTERNS = {
    "assignment": re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?([A-Za-z0-9_\-./+=]{8,})"),
    "bearer": re.compile(r"(?i)bearer\s+([A-Za-z0-9_\-./+=]{12,})"),
}


@dataclass(frozen=True, slots=True)
class SecretFinding:
    path: Path
    line_number: int
    kind: str
    redacted: str


class SecretScannerService:
    def scan(self, root: Path, max_bytes: int = 512_000) -> list[SecretFinding]:
        findings: list[SecretFinding] = []
        for path in _iter_text_files(root):
            if path.stat().st_size > max_bytes:
                continue
            try:
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            for line_number, line in enumerate(lines, start=1):
                for kind, pattern in SECRET_PATTERNS.items():
                    match = pattern.search(line)
                    if match:
                        value = match.group(match.lastindex or 1)
                        findings.append(SecretFinding(path, line_number, kind, redact(value)))
        return findings

    def render_markdown(self, findings: list[SecretFinding]) -> str:
        lines = ["# Secret Scan", ""]
        if not findings:
            return "# Secret Scan\n\nNo likely secrets found.\n"
        for finding in findings:
            lines.append(f"- `{finding.path}:{finding.line_number}` {finding.kind}: `{finding.redacted}`")
        return "\n".join(lines) + "\n"


def redact(value: str) -> str:
    if len(value) <= 6:
        return "****"
    return f"{value[:3]}****{value[-3:]}"


def _iter_text_files(root: Path):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file() and path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif", ".zip", ".exe", ".dll", ".pyc"}:
            yield path

