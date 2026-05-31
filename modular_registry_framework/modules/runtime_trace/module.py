from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_runtime_trace_screen
from .service import RuntimeTraceService


def register(registry: Registry, context: AppContext) -> None:
    service = RuntimeTraceService(context)
    registry.add_module(
        ModuleMetadata(
            name="runtime_trace",
            title="Runtime Trace",
            description="Links runtime events with trace IDs for end-to-end workflow debugging.",
            dependencies=("audit_log",),
        )
    )
    registry.add_service("runtime_trace", service)
    registry.add_command("runtime_trace.new_trace_id", service.new_trace_id)
    registry.add_report_section("runtime_trace.events", "Runtime Trace", lambda ctx: service.render_trace_report(), order=50)
    registry.on("*", service.handle_registry_event)
    registry.add_data_input("runtime_trace", "trace events", "event", "Events carrying a trace_id payload.")
    registry.add_data_output("runtime_trace", "trace report", "records", "Trace event timeline.")
    registry.add_flow("port:runtime_trace:input:trace events", "port:runtime_trace:output:trace report", "collect trace")
    registry.add_screen("System", "Runtime Trace", build_runtime_trace_screen, order=85)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)
