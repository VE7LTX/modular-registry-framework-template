from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_settings_editor_screen
from .service import SettingsEditorService


def register(registry: Registry, context: AppContext) -> None:
    service = SettingsEditorService(context)
    registry.add_module(
        ModuleMetadata(
            name="settings_editor",
            title="Settings Editor",
            description="Shared settings edit/save helpers for CLI, TUI, and Tkinter.",
            dependencies=("settings_manager",),
        )
    )
    registry.add_service("settings_editor", service)
    registry.add_command("settings.edit", service.set_from_text)
    registry.add_command("settings.editor_save", service.save)
    registry.add_data_input("settings_editor", "setting text", "user_input", "Key and raw value text.")
    registry.add_data_output("settings_editor", "settings values", "settings", "Parsed settings values.")
    registry.add_flow("port:settings_editor:input:setting text", "port:settings_editor:output:settings values", "edit settings")
    registry.add_screen("System", "Settings Editor", build_settings_editor_screen, order=31)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

