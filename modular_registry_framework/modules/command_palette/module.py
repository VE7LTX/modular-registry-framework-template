from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_command_palette_screen
from .service import CommandPaletteService


def register(registry: Registry, context: AppContext) -> None:
    service = CommandPaletteService(context)
    registry.add_module(
        ModuleMetadata(
            name="command_palette",
            title="Command Palette",
            description="Searches and runs registered commands.",
            dependencies=("audit_log",),
        )
    )
    registry.add_service("command_palette", service)
    registry.add_command("commands.search", service.search)
    registry.add_command("commands.run", service.run)
    registry.add_data_input("command_palette", "registered commands", "metadata", "Commands registered by modules.")
    registry.add_data_output("command_palette", "command execution", "event", "command.executed events.")
    registry.add_flow("port:command_palette:input:registered commands", "port:command_palette:output:command execution", "run command")
    registry.add_screen("System", "Command Palette", build_command_palette_screen, order=12)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

