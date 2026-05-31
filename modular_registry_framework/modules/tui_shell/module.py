from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_tui_shell_screen
from .service import TuiShellService


def register(registry: Registry, context: AppContext) -> None:
    service = TuiShellService(context)
    registry.add_module(
        ModuleMetadata(
            name="tui_shell",
            title="TUI Shell",
            description="Dependency-free terminal dashboard using shared view models.",
            dependencies=("view_models", "command_palette"),
        )
    )
    registry.add_service("tui_shell", service)
    registry.add_command("tui.render", service.render_dashboard)
    registry.add_data_input("tui_shell", "view models", "view", "Shared table and command view models.")
    registry.add_data_output("tui_shell", "terminal dashboard", "view", "Text dashboard for terminal use.")
    registry.add_flow("port:tui_shell:input:view models", "port:tui_shell:output:terminal dashboard", "render tui")
    registry.add_screen("System", "TUI Preview", build_tui_shell_screen, order=96)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

