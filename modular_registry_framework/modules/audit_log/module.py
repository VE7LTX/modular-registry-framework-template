from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_audit_log_screen
from .service import AuditLogService


def register(registry: Registry, context: AppContext) -> None:
    service = AuditLogService()
    registry.add_module(
        ModuleMetadata(
            name="audit_log",
            title="Audit Log",
            description="Captures recent registry events for traceability and debugging.",
        )
    )
    registry.add_service("audit_log", service)
    registry.on("*", service.handle_registry_event)
    registry.add_data_input("audit_log", "registry events", "event", "Wildcard event stream from registry.emit().")
    registry.add_data_output("audit_log", "audit events", "records", "Recent in-memory event history.")
    registry.add_flow("port:audit_log:input:registry events", "port:audit_log:output:audit events", "record events", "data")
    registry.add_screen("System", "Audit Log", build_audit_log_screen, order=80)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)
