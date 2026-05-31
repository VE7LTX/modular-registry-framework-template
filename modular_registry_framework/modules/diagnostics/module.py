from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_diagnostics_screen
from .service import DiagnosticsService


def register(registry: Registry, context: AppContext) -> None:
    registry.add_module(
        ModuleMetadata(
            name="diagnostics",
            title="Diagnostics",
            description="Switchable debug mode, logging configuration, and runtime inspection.",
            dependencies=("audit_log",),
        )
    )
    registry.add_service("diagnostics", DiagnosticsService(context))
    registry.add_setting("debug.enabled", False, "Debug mode", "Enables verbose diagnostics logging.")
    registry.add_setting("logging.level", "INFO", "Logging level", "DEBUG, INFO, WARNING, ERROR, or CRITICAL.")
    registry.add_setting("logging.console_enabled", True, "Console logging", "Writes logs to stderr/stdout.")
    registry.add_setting("logging.file_enabled", False, "File logging", "Writes logs to logging.file.")
    registry.add_setting("logging.file", "logs/app.log", "Log file", "Relative or absolute log file path.")
    registry.add_screen("System", "Diagnostics", build_diagnostics_screen, order=20)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

