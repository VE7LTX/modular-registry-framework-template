from __future__ import annotations

from pathlib import Path

from modular_registry_framework.core.context import AppContext


class LogViewerService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def log_path(self) -> Path:
        raw_path = Path(str(self.context.settings.get("logging.file", "logs/app.log")))
        return raw_path if raw_path.is_absolute() else self.context.base_dir / raw_path

    def tail(self, lines: int = 100, level: str | None = None, trace_id: str | None = None) -> list[str]:
        path = self.log_path()
        if not path.exists():
            return []
        content = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        if level:
            content = [line for line in content if f" {level.upper()} " in line]
        if trace_id:
            content = [line for line in content if trace_id in line]
        return content[-lines:]

    def render_text(self, lines: int = 100) -> str:
        return "\n".join(self.tail(lines=lines))

