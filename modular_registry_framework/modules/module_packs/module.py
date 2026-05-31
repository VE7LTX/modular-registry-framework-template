from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_module_packs_screen
from .service import ModulePackService


def register(registry: Registry, context: AppContext) -> None:
    service = ModulePackService()
    registry.add_module(
        ModuleMetadata(
            name="module_packs",
            title="Module Packs",
            description="Defines reusable module sets for common app families.",
            dependencies=("template_generator",),
        )
    )
    registry.add_service("module_packs", service)
    registry.add_command("module_packs.render", service.render_markdown)
    registry.add_data_input("module_packs", "template families", "metadata", "Template family module lists.")
    registry.add_data_output("module_packs", "module packs", "metadata", "Named module sets.")
    registry.add_flow("port:module_packs:input:template families", "port:module_packs:output:module packs", "derive packs")
    registry.add_screen("Tools", "Module Packs", build_module_packs_screen, order=55)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

