from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_settings_screen
from .service import SettingsManagerService


def register(registry: Registry, context: AppContext) -> None:
    registry.add_module(
        ModuleMetadata(
            name="settings_manager",
            title="Settings Manager",
            description="Shows registered settings and saves selected values.",
        )
    )
    service = SettingsManagerService(context)
    registry.add_service("settings_manager", service)
    registry.add_command("settings.save", service.save)
    registry.add_screen("System", "Settings", build_settings_screen, order=30)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

