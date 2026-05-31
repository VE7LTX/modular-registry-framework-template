from __future__ import annotations

from modular_registry_framework.core.context import AppContext


class RunbookGeneratorService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def render_markdown(self) -> str:
        modules = self.context.registry.list_modules()
        settings = self.context.registry.list_settings()
        health_checks = self.context.registry.list_health_checks()
        lines = [
            "# Application Runbook",
            "",
            "## Run",
            "",
            "```powershell",
            "python -m modular_registry_framework.main",
            "```",
            "",
            "## Test",
            "",
            "```powershell",
            "python -m compileall modular_registry_framework tests",
            "python -m pytest -q",
            "```",
            "",
            "## Modules",
            "",
        ]
        for metadata in modules.values():
            lines.append(f"- `{metadata.name}`: {metadata.description}")
        lines.extend(["", "## Settings", ""])
        for key, setting in settings.items():
            lines.append(f"- `{key}` default `{setting.default}`: {setting.help_text}")
        lines.extend(["", "## Health Checks", ""])
        for name, check in health_checks.items():
            lines.append(f"- `{name}` ({check.module}): {check.title}")
        lines.extend(["", "## Data Locations", "", "- `settings.json`: local app settings", "- `data/`: local databases", "- `artifacts/`: generated outputs", "- `logs/`: debug logs"])
        return "\n".join(lines) + "\n"

    def save(self, name: str = "RUNBOOK.md"):
        artifacts = self.context.registry.get_service("artifact_library")
        return artifacts.create_text_artifact("docs", name, self.render_markdown())

