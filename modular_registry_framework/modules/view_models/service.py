from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from modular_registry_framework.core.context import AppContext


@dataclass(frozen=True, slots=True)
class TableView:
    title: str
    columns: tuple[str, ...]
    rows: tuple[tuple[Any, ...], ...]

    def render_text(self) -> str:
        lines = [self.title, "=" * len(self.title)]
        lines.append(" | ".join(self.columns))
        lines.append(" | ".join("---" for _ in self.columns))
        for row in self.rows:
            lines.append(" | ".join(str(value) for value in row))
        return "\n".join(lines)


class ViewModelService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def modules_table(self) -> TableView:
        rows = tuple(
            (metadata.name, metadata.title, ", ".join(metadata.dependencies) or "none")
            for metadata in self.context.registry.list_modules().values()
        )
        return TableView("Modules", ("Name", "Title", "Dependencies"), rows)

    def health_table(self) -> TableView:
        rows = tuple(
            (result.status, result.name, result.message)
            for result in self.context.registry.get_service("health_checks").run_all()
        )
        return TableView("Health", ("Status", "Name", "Message"), rows)

    def commands_table(self) -> TableView:
        rows = tuple((name,) for name in sorted(self.context.registry.list_commands()))
        return TableView("Commands", ("Name",), rows)

    def artifacts_table(self) -> TableView:
        artifacts = self.context.registry.get_service("artifact_library").list_artifacts()
        rows = tuple((artifact.kind, artifact.name, artifact.path, artifact.trace_id or "") for artifact in artifacts)
        return TableView("Artifacts", ("Kind", "Name", "Path", "Trace"), rows)

