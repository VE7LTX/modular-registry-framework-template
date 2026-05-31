from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_reports_screen
from .service import ReportService, render_module_inventory, render_registered_capabilities


def register(registry: Registry, context: AppContext) -> None:
    registry.add_module(
        ModuleMetadata(
            name="reports",
            title="Reports",
            description="Renders Markdown reports from sections contributed by modules.",
            dependencies=("artifact_library",),
        )
    )
    service = ReportService(context)
    registry.add_service("reports", service)
    registry.add_command("reports.render_markdown", service.render_markdown)
    registry.add_command("reports.save_markdown", service.save_markdown)
    registry.add_report_section("modules.inventory", "Module Inventory", render_module_inventory, order=10)
    registry.add_report_section(
        "modules.capabilities",
        "Registered Capabilities",
        render_registered_capabilities,
        order=20,
    )
    registry.add_screen("Tools", "Reports", build_reports_screen, order=30)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

