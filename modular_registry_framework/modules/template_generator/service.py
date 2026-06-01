from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from modular_registry_framework.core.context import AppContext


@dataclass(frozen=True, slots=True)
class AppTemplate:
    name: str
    title: str
    description: str
    modules: tuple[str, ...]
    folders: tuple[str, ...]


APP_TEMPLATES = {
    "desktop_workflow": AppTemplate(
        "desktop_workflow",
        "Desktop Workflow App",
        "Tkinter/local workflow tool with records, imports, jobs, reports, and artifacts.",
        ("dashboard", "help", "settings_manager", "diagnostics", "health_checks", "records", "jobs", "reports"),
        ("data", "artifacts/reports", "artifacts/exports", "docs", "tests"),
    ),
    "data_ingestion": AppTemplate(
        "data_ingestion",
        "Data Ingestion App",
        "API/file ingestion app with storage, importers, exporters, audit, and health checks.",
        ("storage", "importers", "exporters", "api_clients", "audit_log", "runtime_trace", "reports"),
        ("data/raw", "data/normalized", "artifacts/imports", "artifacts/reports", "tests"),
    ),
    "case_workspace": AppTemplate(
        "case_workspace",
        "Case Or Project Workspace",
        "Folder/artifact-heavy workspace for records, notes, reports, and exports.",
        ("records", "artifact_library", "importers", "exporters", "reports", "runtime_trace"),
        ("cases", "artifacts/reports", "artifacts/exports", "docs", "tests"),
    ),
    "ai_agent_tool": AppTemplate(
        "ai_agent_tool",
        "AI Agent Tool",
        "Local AI/agent tool with settings, secrets, API clients, traces, jobs, and eval reports.",
        ("env_secrets", "api_clients", "jobs", "runtime_trace", "artifact_library", "reports", "diagnostics"),
        ("prompts", "memory", "artifacts/traces", "artifacts/reports", "tests"),
    ),
    "benchmark_evaluation": AppTemplate(
        "benchmark_evaluation",
        "Benchmark Evaluation App",
        "Repeatable benchmark harness with jobs, artifacts, imports, exports, and reports.",
        ("jobs", "artifact_library", "importers", "exporters", "reports", "runtime_trace", "health_checks"),
        ("configs", "prompts", "results", "artifacts/reports", "tests"),
    ),
    "integration_control_panel": AppTemplate(
        "integration_control_panel",
        "Integration Control Panel",
        "Dashboard/control panel for APIs, secrets, health, jobs, logs, and reports.",
        ("api_clients", "env_secrets", "health_checks", "jobs", "diagnostics", "audit_log", "reports"),
        ("configs", "logs", "artifacts/api", "artifacts/reports", "tests"),
    ),
    "cli_tool": AppTemplate(
        "cli_tool",
        "CLI Tool",
        "Automation-first command utility with settings, scans, project repair, recipes, and tests.",
        ("command_palette", "settings_editor", "project_repair", "workspace_scanner", "secret_scanner", "recipes"),
        ("configs", "scripts", "artifacts/reports", "docs", "tests"),
    ),
    "tui_tool": AppTemplate(
        "tui_tool",
        "TUI Tool",
        "Terminal-first app with dashboard rendering, command search, logs, artifacts, and workflows.",
        ("tui_shell", "view_models", "command_palette", "health_checks", "log_viewer", "artifact_browser", "workflows"),
        ("configs", "logs", "artifacts/reports", "artifacts/exports", "tests"),
    ),
    "tkinter_tool": AppTemplate(
        "tkinter_tool",
        "Tkinter Tool",
        "Local desktop shell with reusable screens, settings, jobs, reports, and artifact browsing.",
        ("dashboard", "ui_adapters", "view_models", "settings_editor", "jobs", "reports", "artifact_browser"),
        ("data", "logs", "artifacts/reports", "artifacts/exports", "docs", "tests"),
    ),
}


class TemplateGeneratorService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def list_templates(self) -> dict[str, AppTemplate]:
        return dict(APP_TEMPLATES)

    def create_app(self, template_name: str, target_dir: Path) -> Path:
        template = APP_TEMPLATES[template_name]
        target_dir.mkdir(parents=True, exist_ok=True)
        for folder in template.folders:
            (target_dir / folder).mkdir(parents=True, exist_ok=True)

        readme = _render_readme(template)
        settings = _render_settings(template)
        modules = _render_modules_file(template)
        (target_dir / "README.md").write_text(readme, encoding="utf-8")
        (target_dir / "settings.json").write_text(settings, encoding="utf-8")
        (target_dir / "modules.txt").write_text(modules, encoding="utf-8")
        (target_dir / "docs").mkdir(parents=True, exist_ok=True)
        (target_dir / "docs" / "flow.md").write_text(_render_flow_doc(template), encoding="utf-8")
        self.context.registry.emit(
            "template.generated",
            {"template": template.name, "target_dir": str(target_dir)},
        )
        return target_dir


def _render_readme(template: AppTemplate) -> str:
    modules = "\n".join(f"- `{module}`" for module in template.modules)
    return f"""# {template.title}

{template.description}

## Included Modules

{modules}

## Next Steps

1. Copy the template into a real app package.
2. Keep only the modules needed for the first slice.
3. Add domain-specific feature modules.
4. Run tests before adding UI complexity.
"""


def _render_settings(template: AppTemplate) -> str:
    return """{
  "debug.enabled": false,
  "logging.level": "INFO",
  "logging.console_enabled": true,
  "logging.file_enabled": false,
  "logging.file": "logs/app.log"
}
"""


def _render_modules_file(template: AppTemplate) -> str:
    return "\n".join(template.modules) + "\n"


def _render_flow_doc(template: AppTemplate) -> str:
    modules = " --> ".join(template.modules)
    return f"""# Initial Flow

```mermaid
flowchart LR
  {modules}
```
"""
