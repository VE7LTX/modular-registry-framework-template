from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_artifact_library_screen
from .service import ArtifactLibraryService


def register(registry: Registry, context: AppContext) -> None:
    registry.add_module(
        ModuleMetadata(
            name="artifact_library",
            title="Artifact Library",
            description="Creates and tracks generated files in predictable artifact folders.",
            dependencies=("audit_log",),
        )
    )
    registry.add_service("artifact_library", ArtifactLibraryService(context))
    registry.add_data_input("artifact_library", "artifact content", "file", "Generated text or external files.")
    registry.add_data_output("artifact_library", "artifact records", "records", "Tracked generated or external artifacts.")
    registry.add_flow(
        "port:artifact_library:input:artifact content",
        "port:artifact_library:output:artifact records",
        "track artifact",
        "data",
    )
    registry.add_flow("port:artifact_library:output:artifact records", "event:artifact.created", "emit artifact event", "event")
    registry.add_screen("System", "Artifacts", build_artifact_library_screen, order=70)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)
