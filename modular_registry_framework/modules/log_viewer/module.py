from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_log_viewer_screen
from .service import LogViewerService


def register(registry: Registry, context: AppContext) -> None:
    service = LogViewerService(context)
    registry.add_module(
        ModuleMetadata(
            name="log_viewer",
            title="Log Viewer",
            description="Tails and filters the configured app log.",
            dependencies=("diagnostics",),
        )
    )
    registry.add_service("log_viewer", service)
    registry.add_command("logs.tail", service.tail)
    registry.add_data_input("log_viewer", "log file", "file", "Configured application log file.")
    registry.add_data_output("log_viewer", "log lines", "view", "Filtered log lines.")
    registry.add_flow("port:log_viewer:input:log file", "port:log_viewer:output:log lines", "tail logs")
    registry.add_screen("System", "Logs", build_log_viewer_screen, order=97)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

