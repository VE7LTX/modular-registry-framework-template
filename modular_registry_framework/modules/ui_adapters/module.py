from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_ui_adapters_screen
from .service import UiAdapterService


def register(registry: Registry, context: AppContext) -> None:
    service = UiAdapterService(context)
    registry.add_module(
        ModuleMetadata(
            name="ui_adapters",
            title="UI Adapters",
            description="Maps registered modules to CLI, TUI, Tkinter, dashboard, and report surfaces.",
            dependencies=("view_models", "command_palette"),
        )
    )
    registry.add_service("ui_adapters", service)
    registry.add_command("ui_adapters.render", service.render_text)
    registry.add_data_input("ui_adapters", "registry surfaces", "metadata", "Commands, screens, reports, and modules.")
    registry.add_data_output("ui_adapters", "surface map", "view", "Capability coverage across app surfaces.")
    registry.add_flow("port:ui_adapters:input:registry surfaces", "port:ui_adapters:output:surface map", "map surfaces")
    registry.add_screen("System", "UI Adapters", build_ui_adapters_screen, order=96)
    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

