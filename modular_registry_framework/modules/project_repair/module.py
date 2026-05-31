from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_project_repair_screen
from .service import ProjectRepairService


def register(registry: Registry, context: AppContext) -> None:
    service = ProjectRepairService()
    registry.add_module(
        ModuleMetadata(
            name="project_repair",
            title="Project Repair",
            description="Plans and creates missing baseline project files.",
            dependencies=("workspace_scanner", "secret_scanner"),
        )
    )
    registry.add_service("project_repair", service)
    registry.add_command("project_repair.plan", service.plan)
    registry.add_command("project_repair.apply", service.apply_baseline)
    registry.add_data_input("project_repair", "project folder", "file", "Project folder to repair.")
    registry.add_data_output("project_repair", "baseline files", "file", "README, gitignore, env example, docs, tests.")
    registry.add_flow("port:project_repair:input:project folder", "port:project_repair:output:baseline files", "repair project")
    registry.add_screen("Tools", "Project Repair", build_project_repair_screen, order=100)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

