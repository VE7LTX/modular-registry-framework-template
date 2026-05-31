from __future__ import annotations

from pathlib import Path

from modular_registry_framework.core.context import AppContext


class ArtifactBrowserService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def list_files(self) -> list[Path]:
        root = self.context.base_dir / "artifacts"
        if not root.exists():
            return []
        return sorted(path for path in root.rglob("*") if path.is_file())

    def preview(self, path: Path, max_chars: int = 8000) -> str:
        if path.suffix.lower() not in {".txt", ".md", ".json", ".jsonl", ".xml", ".yaml", ".yml", ".log", ".mmd"}:
            return f"Preview unavailable for {path.suffix or 'file'}"
        return path.read_text(encoding="utf-8", errors="ignore")[:max_chars]

    def render_index(self) -> str:
        return "\n".join(str(path) for path in self.list_files())

