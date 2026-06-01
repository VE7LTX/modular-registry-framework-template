from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AppProfile:
    name: str
    title: str
    description: str
    modules: tuple[str, ...]
    entrypoints: tuple[str, ...]


PROFILES = {
    "tui_tool": AppProfile(
        "tui_tool",
        "TUI Tool",
        "Terminal-first utility with command search, logs, artifacts, health, and workflows.",
        ("tui_shell", "command_palette", "view_models", "health_checks", "log_viewer", "artifact_browser", "workflows"),
        ("mrf tui", "mrf commands", "mrf workflows"),
    ),
    "cli_tool": AppProfile(
        "cli_tool",
        "CLI Tool",
        "Automation-first command tool with settings, repair helpers, scans, recipes, and tests.",
        ("command_palette", "settings_editor", "project_repair", "workspace_scanner", "secret_scanner", "recipes"),
        ("mrf commands", "mrf settings", "mrf repair", "mrf recipes"),
    ),
    "tkinter_tool": AppProfile(
        "tkinter_tool",
        "Tkinter Tool",
        "Local desktop shell with shared view models, screens, settings, jobs, reports, and artifacts.",
        ("dashboard", "ui_adapters", "view_models", "settings_editor", "jobs", "reports", "artifact_browser"),
        ("python -m modular_registry_framework",),
    ),
    "agent_lab": AppProfile(
        "agent_lab",
        "Agent Lab",
        "Local AI/agent experimentation with traces, jobs, artifacts, prompts, eval recipes, and exports.",
        ("runtime_trace", "trace_graph", "jobs", "artifact_library", "recipes", "exporters", "reports"),
        ("mrf recipes agent_eval", "mrf trace-graph"),
    ),
    "data_api_tool": AppProfile(
        "data_api_tool",
        "Data/API Tool",
        "API and file ingestion with secrets, clients, storage, imports, exports, workflows, and reports.",
        ("env_secrets", "api_clients", "storage", "importers", "exporters", "workflows", "reports"),
        ("mrf health", "mrf workflows api_sync_review"),
    ),
}


class AppProfileService:
    def list_profiles(self) -> dict[str, AppProfile]:
        return dict(PROFILES)

    def render(self, name: str | None = None) -> str:
        profiles = [PROFILES[name]] if name else PROFILES.values()
        lines: list[str] = []
        for profile in profiles:
            lines.extend([f"# {profile.title}", "", profile.description, ""])
            lines.append("Modules: " + ", ".join(f"`{module}`" for module in profile.modules))
            lines.append("Entrypoints: " + ", ".join(f"`{entrypoint}`" for entrypoint in profile.entrypoints))
            lines.append("")
        return "\n".join(lines).strip()

    def modules_for(self, name: str) -> tuple[str, ...]:
        return PROFILES[name].modules

