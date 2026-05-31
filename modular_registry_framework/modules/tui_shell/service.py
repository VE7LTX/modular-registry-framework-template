from __future__ import annotations

from modular_registry_framework.core.context import AppContext


class TuiShellService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def render_dashboard(self) -> str:
        view_models = self.context.registry.get_service("view_models")
        sections = [
            "Modular Registry Framework TUI",
            "",
            view_models.modules_table().render_text(),
            "",
            view_models.health_table().render_text(),
            "",
            "Commands",
            "========",
            self.context.registry.get_service("command_palette").render_text(),
        ]
        return "\n".join(sections)

    def run_once(self) -> str:
        return self.render_dashboard()

