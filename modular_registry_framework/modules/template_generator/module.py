from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_template_generator_screen
from .service import TemplateGeneratorService


def register(registry: Registry, context: AppContext) -> None:
    service = TemplateGeneratorService(context)
    registry.add_module(
        ModuleMetadata(
            name="template_generator",
            title="Template Generator",
            description="Creates starter app folders for common application families.",
            dependencies=("artifact_library", "flow_graph"),
        )
    )
    registry.add_service("template_generator", service)
    registry.add_command("template_generator.create_app", service.create_app)
    registry.add_data_input("template_generator", "template selection", "user_input", "Selected starter app family.")
    registry.add_data_output("template_generator", "app starter folder", "file", "Generated starter README/settings/folders.")
    registry.add_flow(
        "port:template_generator:input:template selection",
        "port:template_generator:output:app starter folder",
        "generate app starter",
    )
    registry.add_screen("Tools", "Template Generator", build_template_generator_screen, order=50)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

