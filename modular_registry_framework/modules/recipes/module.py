from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_recipes_screen
from .service import RecipeService


def register(registry: Registry, context: AppContext) -> None:
    service = RecipeService(context)
    registry.add_module(
        ModuleMetadata(
            name="recipes",
            title="Recipes",
            description="Provides runnable examples that exercise cross-module flows.",
            dependencies=("workflows", "artifact_library", "runtime_trace"),
        )
    )
    registry.add_service("recipes", service)
    registry.add_command("recipes.render", service.render)
    registry.add_command("recipes.run", service.run)
    registry.add_data_input("recipes", "recipe name", "metadata", "Named example flow.")
    registry.add_data_output("recipes", "recipe artifact", "file", "Generated proof artifact and trace.")
    registry.add_flow("port:recipes:input:recipe name", "port:recipes:output:recipe artifact", "run recipe")
    registry.add_screen("Examples", "Recipes", build_recipes_screen, order=20)
    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)
