from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_trace_graph_screen
from .service import TraceGraphService


def register(registry: Registry, context: AppContext) -> None:
    service = TraceGraphService(context)
    registry.add_module(
        ModuleMetadata(
            name="trace_graph",
            title="Trace Graph",
            description="Renders actual runtime trace events as text or Mermaid graph.",
            dependencies=("runtime_trace",),
        )
    )
    registry.add_service("trace_graph", service)
    registry.add_command("trace_graph.render", service.render_text)
    registry.add_command("trace_graph.mermaid", service.render_mermaid)
    registry.add_data_input("trace_graph", "trace events", "event", "Runtime events with trace IDs.")
    registry.add_data_output("trace_graph", "run graph", "graph", "Actual run-history graph.")
    registry.add_flow("port:trace_graph:input:trace events", "port:trace_graph:output:run graph", "render run history")
    registry.add_report_section("trace_graph.runtime", "Runtime Trace Graph", lambda context: service.render_text(), order=35)
    registry.add_screen("System", "Trace Graph", build_trace_graph_screen, order=64)
    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

