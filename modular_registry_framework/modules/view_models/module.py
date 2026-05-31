from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_view_models_screen
from .service import ViewModelService


def register(registry: Registry, context: AppContext) -> None:
    service = ViewModelService(context)
    registry.add_module(
        ModuleMetadata(
            name="view_models",
            title="View Models",
            description="Shared display models for CLI, TUI, and Tkinter surfaces.",
            dependencies=("health_checks", "artifact_library"),
        )
    )
    registry.add_service("view_models", service)
    registry.add_command("view.modules", service.modules_table)
    registry.add_command("view.health", service.health_table)
    registry.add_data_input("view_models", "registry data", "metadata", "Registry state and service summaries.")
    registry.add_data_output("view_models", "table views", "view", "Shared display models.")
    registry.add_flow("port:view_models:input:registry data", "port:view_models:output:table views", "shape display data")
    registry.add_screen("System", "View Models", build_view_models_screen, order=95)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

