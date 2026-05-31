from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_help_screen
from .service import HelpService


def register(registry: Registry, context: AppContext) -> None:
    registry.add_module(
        ModuleMetadata(
            name="help",
            title="Help",
            description="Collects module-owned help topics into a browsable help screen.",
        )
    )
    service = HelpService(context)
    registry.add_service("help", service)
    registry.add_command("help.render_topic_index", service.render_topic_index)
    registry.add_screen("System", "Help", build_help_screen, order=10)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

