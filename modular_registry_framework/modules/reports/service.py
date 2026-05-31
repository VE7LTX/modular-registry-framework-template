from __future__ import annotations

import logging
from datetime import datetime, timezone

from modular_registry_framework.core.context import AppContext


class ReportService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def render_markdown(self, title: str = "Application Report") -> str:
        logging.getLogger(__name__).debug("Rendering Markdown report: title=%s", title)
        lines = [
            f"# {title}",
            "",
            f"Generated: {datetime.now(timezone.utc).isoformat()}",
            "",
        ]
        for section in self.context.registry.list_report_sections():
            logging.getLogger(__name__).debug("Rendering report section: %s", section.name)
            lines.extend([f"## {section.title}", "", section.renderer(self.context), ""])
        return "\n".join(lines)

    def save_markdown(self, name: str = "app-report.md", title: str = "Application Report"):
        logging.getLogger(__name__).debug("Saving Markdown report: name=%s title=%s", name, title)
        content = self.render_markdown(title)
        artifact_library = self.context.registry.get_service("artifact_library")
        record = artifact_library.create_text_artifact("reports", name, content)
        self.context.registry.emit("report.generated", {"path": str(record.path), "title": title})
        return record


def render_module_inventory(context: AppContext) -> str:
    lines = []
    for metadata in context.registry.list_modules().values():
        dependencies = ", ".join(metadata.dependencies) if metadata.dependencies else "none"
        lines.append(f"- **{metadata.title}** (`{metadata.name}`): {metadata.description} Dependencies: {dependencies}.")
    return "\n".join(lines)


def render_registered_capabilities(context: AppContext) -> str:
    services = ", ".join(sorted(context.registry.list_services())) or "none"
    importers = ", ".join(sorted(context.registry.list_file_importers())) or "none"
    report_sections = ", ".join(section.name for section in context.registry.list_report_sections()) or "none"
    return "\n".join(
        [
            f"- Services: {services}",
            f"- Importers: {importers}",
            f"- Report sections: {report_sections}",
        ]
    )
