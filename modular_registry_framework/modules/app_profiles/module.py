from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_app_profiles_screen
from .service import AppProfileService


def register(registry: Registry, context: AppContext) -> None:
    service = AppProfileService()
    registry.add_module(
        ModuleMetadata(
            name="app_profiles",
            title="App Profiles",
            description="Defines opinionated module bundles for common app modes.",
            dependencies=("template_generator", "module_packs"),
        )
    )
    registry.add_service("app_profiles", service)
    registry.add_command("app_profiles.render", service.render)
    registry.add_data_input("app_profiles", "app mode", "metadata", "Named app type.")
    registry.add_data_output("app_profiles", "module bundle", "metadata", "Recommended module set and entrypoints.")
    registry.add_flow("port:app_profiles:input:app mode", "port:app_profiles:output:module bundle", "select modules")
    registry.add_screen("Tools", "App Profiles", build_app_profiles_screen, order=16)
    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

