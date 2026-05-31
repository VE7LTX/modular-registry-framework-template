from __future__ import annotations

from modular_registry_framework.core.context import AppContext


class HelpService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def list_topics(self) -> dict[str, str]:
        return self.context.registry.list_help_topics()

    def render_topic_index(self) -> str:
        lines = ["# Help Topics", ""]
        for key, content in sorted(self.list_topics().items()):
            lines.extend([f"## {key}", "", content, ""])
        return "\n".join(lines)

