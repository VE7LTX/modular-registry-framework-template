from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_dashboard_screen
from .service import DashboardService


def register(registry: Registry, context: AppContext) -> None:
    registry.add_module(
        ModuleMetadata(
            name="dashboard",
            title="Dashboard",
            description="Shows the live map of registered modules and capabilities.",
            dependencies=("help",),
        )
    )
    service = DashboardService(context)
    registry.add_service("dashboard", service)
    registry.add_command("dashboard.render_text", service.render_text)
    registry.add_screen("System", "Dashboard", build_dashboard_screen, order=0)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

