from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_artifact_browser_screen
from .service import ArtifactBrowserService


def register(registry: Registry, context: AppContext) -> None:
    service = ArtifactBrowserService(context)
    registry.add_module(
        ModuleMetadata(
            name="artifact_browser",
            title="Artifact Browser",
            description="Lists and previews generated artifacts.",
            dependencies=("artifact_library",),
        )
    )
    registry.add_service("artifact_browser", service)
    registry.add_command("artifacts.list", service.list_files)
    registry.add_command("artifacts.preview", service.preview)
    registry.add_data_input("artifact_browser", "artifact files", "file", "Files under artifacts/.")
    registry.add_data_output("artifact_browser", "artifact previews", "view", "Text previews and indexes.")
    registry.add_flow("port:artifact_browser:input:artifact files", "port:artifact_browser:output:artifact previews", "preview artifacts")
    registry.add_screen("System", "Artifact Browser", build_artifact_browser_screen, order=75)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

