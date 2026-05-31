from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_graph_export_screen
from .service import GraphExportService, render_graph_export_report


def register(registry: Registry, context: AppContext) -> None:
    service = GraphExportService(context)
    registry.add_module(
        ModuleMetadata(
            name="graph_export",
            title="Graph Export",
            description="Saves flow graph snapshots as Mermaid and JSON artifacts.",
            dependencies=("flow_graph", "artifact_library"),
        )
    )
    registry.add_service("graph_export", service)
    registry.add_command("graph_export.save_mermaid", service.save_mermaid)
    registry.add_command("graph_export.save_json", service.save_json)
    registry.add_report_section("system.graph_export", "Graph Export", render_graph_export_report, order=60)
    registry.add_data_input("graph_export", "flow graph", "diagram", "Current automatic flow graph.")
    registry.add_data_output("graph_export", "graph artifacts", "file", "Mermaid and JSON graph snapshots.")
    registry.add_flow("port:graph_export:input:flow graph", "port:graph_export:output:graph artifacts", "persist graph")
    registry.add_screen("System", "Graph Export", build_graph_export_screen, order=6)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

