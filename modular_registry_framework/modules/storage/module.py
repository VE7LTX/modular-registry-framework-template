from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_storage_screen
from .service import StorageService, render_storage_report


def register(registry: Registry, context: AppContext) -> None:
    service = StorageService(context)
    registry.add_module(
        ModuleMetadata(
            name="storage",
            title="Storage",
            description="Provides SQLite lifecycle helpers, health checks, and backups.",
            dependencies=("health_checks", "artifact_library"),
        )
    )
    registry.add_service("storage", service)
    registry.add_command("storage.initialize", service.initialize)
    registry.add_command("storage.backup", service.backup)
    registry.add_health_check("storage.sqlite", "SQLite storage", service.health_check, "storage")
    registry.add_report_section("storage.sqlite", "Storage", render_storage_report, order=40)
    registry.add_data_input("storage", "database path", "settings", "SQLite database path.")
    registry.add_data_output("storage", "sqlite database", "file", "Local SQLite database file.")
    registry.add_flow("port:storage:input:database path", "port:storage:output:sqlite database", "open database")
    registry.add_screen("System", "Storage", build_storage_screen, order=45)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

