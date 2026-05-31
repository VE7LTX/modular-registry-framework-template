from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import Registry

from .help import HELP_TOPICS
from .screens import build_example_screen
from .service import ExampleService


def register(registry: Registry, context: AppContext) -> None:
    registry.add_service("example", ExampleService(registry))
    registry.add_screen("Examples", "Example Module", build_example_screen, order=10)
    registry.add_setting(
        "example.default_status",
        "New",
        "Default example item status",
        "Used when new example records are created.",
    )

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

