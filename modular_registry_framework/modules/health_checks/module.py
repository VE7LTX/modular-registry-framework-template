from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_health_checks_screen
from .service import HealthCheckService, dependency_integrity_check, modules_registered_check, trace_ports_check


def register(registry: Registry, context: AppContext) -> None:
    registry.add_module(
        ModuleMetadata(
            name="health_checks",
            title="Health Checks",
            description="Runs readiness checks for modules, configuration, traceability, and integrations.",
            dependencies=("audit_log",),
        )
    )
    registry.add_service("health_checks", HealthCheckService(context))
    registry.add_health_check("modules.registered", "Modules registered", modules_registered_check, "health_checks")
    registry.add_health_check("modules.dependencies", "Module dependencies", dependency_integrity_check, "health_checks")
    registry.add_health_check("trace.ports", "Trace ports declared", trace_ports_check, "health_checks")
    registry.add_data_input("health_checks", "registered checks", "metadata", "Health checks contributed by modules.")
    registry.add_data_output("health_checks", "health results", "records", "Pass/warn/fail readiness results.")
    registry.add_flow("port:health_checks:input:registered checks", "port:health_checks:output:health results", "run checks")
    registry.add_flow("port:health_checks:output:health results", "event:health.checked", "emit health event", "event")
    registry.add_screen("System", "Health", build_health_checks_screen, order=15)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)
