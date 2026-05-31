from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_flow_graph_screen
from .service import FlowGraphService


def register(registry: Registry, context: AppContext) -> None:
    registry.add_module(
        ModuleMetadata(
            name="flow_graph",
            title="Flow Graph",
            description="Builds an automatic trace graph of modules, capabilities, events, inputs, and outputs.",
            dependencies=("dashboard", "audit_log"),
        )
    )
    service = FlowGraphService(context)
    registry.add_service("flow_graph", service)
    registry.add_command("flow_graph.render_mermaid", service.render_mermaid)
    registry.add_command("flow_graph.render_adjacency", service.render_adjacency)
    registry.add_report_section("system.flow_graph", "System Flow Graph", lambda ctx: service.render_mermaid(), order=30)
    registry.add_screen("System", "Flow Graph", build_flow_graph_screen, order=5)
    registry.add_data_input("flow_graph", "registry capabilities", "metadata", "Registered modules and capabilities.")
    registry.add_data_output("flow_graph", "mermaid graph", "diagram", "Renderable Mermaid flowchart.")

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

