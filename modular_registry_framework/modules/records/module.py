from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_records_screen
from .service import RecordService


def register(registry: Registry, context: AppContext) -> None:
    registry.add_module(
        ModuleMetadata(
            name="records",
            title="Records",
            description="Provides a generic list/detail/archive record pattern.",
            dependencies=("audit_log",),
        )
    )
    registry.add_service("records", RecordService(context))
    registry.add_data_input("records", "record values", "records", "Typed or generic values from feature modules.")
    registry.add_data_output("records", "record events", "event", "record.created and record.archived events.")
    registry.add_flow("port:records:input:record values", "port:records:output:record events", "store records", "data")
    registry.add_screen("Tools", "Records", build_records_screen, order=10)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

