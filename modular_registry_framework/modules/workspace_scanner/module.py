from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_workspace_scanner_screen
from .service import WorkspaceScannerService


def register(registry: Registry, context: AppContext) -> None:
    service = WorkspaceScannerService()
    registry.add_module(
        ModuleMetadata(
            name="workspace_scanner",
            title="Workspace Scanner",
            description="Scans local project folders and summarizes project health signals.",
            dependencies=("reports",),
        )
    )
    registry.add_service("workspace_scanner", service)
    registry.add_command("workspace.scan", service.scan_workspace)
    registry.add_data_input("workspace_scanner", "workspace folder", "file", "Folder containing project directories.")
    registry.add_data_output("workspace_scanner", "project inventory", "records", "Detected project signals.")
    registry.add_flow("port:workspace_scanner:input:workspace folder", "port:workspace_scanner:output:project inventory", "scan projects")
    registry.add_screen("Tools", "Workspace Scanner", build_workspace_scanner_screen, order=60)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

