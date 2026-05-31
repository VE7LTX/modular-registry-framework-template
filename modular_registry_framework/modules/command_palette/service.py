from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from modular_registry_framework.core.context import AppContext


@dataclass(frozen=True, slots=True)
class CommandInfo:
    name: str


class CommandPaletteService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def search(self, query: str = "") -> list[CommandInfo]:
        clean_query = query.strip().lower()
        names = sorted(self.context.registry.list_commands())
        if clean_query:
            names = [name for name in names if clean_query in name.lower()]
        return [CommandInfo(name) for name in names]

    def run(self, name: str, *args, **kwargs) -> Any:
        command = self.context.registry.get_command(name)
        result = command(*args, **kwargs)
        self.context.registry.emit("command.executed", {"name": name})
        return result

    def render_text(self, query: str = "") -> str:
        return "\n".join(command.name for command in self.search(query))

