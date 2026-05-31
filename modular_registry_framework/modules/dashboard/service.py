from __future__ import annotations

from modular_registry_framework.core.context import AppContext


class DashboardService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def snapshot(self) -> dict:
        registry = self.context.registry
        return {
            "modules": registry.list_modules(),
            "services": registry.list_services(),
            "screens": registry.list_screens(),
            "settings": registry.list_settings(),
            "commands": registry.list_commands(),
            "importers": registry.list_file_importers(),
            "report_sections": registry.list_report_sections(),
            "event_handlers": registry.list_event_handlers(),
        }

    def render_text(self) -> str:
        snapshot = self.snapshot()
        lines = ["Application Dashboard", ""]
        lines.append("Modules:")
        for metadata in snapshot["modules"].values():
            lines.append(f"- {metadata.title} ({metadata.name}): {metadata.description}")
        lines.extend(["", "Services: " + ", ".join(sorted(snapshot["services"]))])
        lines.append("Importers: " + ", ".join(sorted(snapshot["importers"])))
        lines.append("Report sections: " + ", ".join(section.name for section in snapshot["report_sections"]))
        lines.append("Event handlers: " + str(snapshot["event_handlers"]))
        return "\n".join(lines)

