from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_runbook_generator_screen
from .service import RunbookGeneratorService


def register(registry: Registry, context: AppContext) -> None:
    service = RunbookGeneratorService(context)
    registry.add_module(
        ModuleMetadata(
            name="runbook_generator",
            title="Runbook Generator",
            description="Generates operational runbooks from registered app metadata.",
            dependencies=("artifact_library", "health_checks"),
        )
    )
    registry.add_service("runbook_generator", service)
    registry.add_command("runbook.render", service.render_markdown)
    registry.add_command("runbook.save", service.save)
    registry.add_data_input("runbook_generator", "registry metadata", "metadata", "Modules, settings, checks, and paths.")
    registry.add_data_output("runbook_generator", "runbook", "artifact", "Generated Markdown runbook.")
    registry.add_flow("port:runbook_generator:input:registry metadata", "port:runbook_generator:output:runbook", "generate runbook")
    registry.add_screen("Tools", "Runbook", build_runbook_generator_screen, order=90)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

