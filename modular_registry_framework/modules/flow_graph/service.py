from __future__ import annotations

import re

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.modules.health_checks.models import HealthResult

from .models import FlowGraph, GraphEdge, GraphNode


class FlowGraphService:
    """Build an inspectable graph from registry declarations and inferred links."""

    def __init__(self, context: AppContext) -> None:
        self.context = context

    def build_graph(self) -> FlowGraph:
        nodes: dict[str, GraphNode] = {}
        edges: set[GraphEdge] = set()
        registry = self.context.registry

        for module_name, metadata in registry.list_modules().items():
            module_id = _node_id(f"module:{module_name}")
            nodes[module_id] = GraphNode(module_id, metadata.title, "module")

            for dependency in metadata.dependencies:
                dependency_id = _node_id(f"module:{dependency}")
                nodes.setdefault(dependency_id, GraphNode(dependency_id, dependency, "module"))
                edges.add(GraphEdge(dependency_id, module_id, "dependency", "dependency"))

        for service_name in registry.list_services():
            module_id = _node_id(f"module:{service_name}")
            service_id = _node_id(f"service:{service_name}")
            nodes.setdefault(module_id, GraphNode(module_id, service_name, "module"))
            nodes[service_id] = GraphNode(service_id, service_name, "service")
            edges.add(GraphEdge(module_id, service_id, "provides", "capability"))

        for screen in registry.list_screens():
            screen_id = _node_id(f"screen:{screen.area}:{screen.title}")
            nodes[screen_id] = GraphNode(screen_id, f"{screen.area}: {screen.title}", "screen")
            if screen.title:
                inferred_module = _infer_module_from_title(screen.title, registry.list_modules())
                if inferred_module:
                    edges.add(GraphEdge(_node_id(f"module:{inferred_module}"), screen_id, "shows", "ui"))

        for key in registry.list_settings():
            setting_id = _node_id(f"setting:{key}")
            nodes[setting_id] = GraphNode(setting_id, key, "setting")
            module_name = key.split(".", 1)[0]
            if module_name in registry.list_modules():
                edges.add(GraphEdge(_node_id(f"module:{module_name}"), setting_id, "configures", "settings"))

        for extension, importer in registry.list_file_importers().items():
            importer_id = _node_id(f"importer:{extension}")
            nodes[importer_id] = GraphNode(importer_id, f"{extension} {importer.label}", "importer")
            nodes.setdefault(_node_id("event:file.imported"), GraphNode(_node_id("event:file.imported"), "file.imported", "event"))
            edges.add(GraphEdge(importer_id, _node_id("event:file.imported"), "emits", "event"))

        for format_name, exporter in registry.list_exporters().items():
            exporter_id = _node_id(f"exporter:{format_name}")
            nodes[exporter_id] = GraphNode(exporter_id, f"{format_name} {exporter.extension}", "exporter")
            nodes.setdefault(_node_id("event:data.exported"), GraphNode(_node_id("event:data.exported"), "data.exported", "event"))
            edges.add(GraphEdge(exporter_id, _node_id("event:data.exported"), "emits", "event"))

        for name, api_client in registry.list_api_clients().items():
            api_id = _node_id(f"api_client:{name}")
            nodes[api_id] = GraphNode(api_id, api_client.label, "api_client")

        for name, health_check in registry.list_health_checks().items():
            check_id = _node_id(f"health_check:{name}")
            nodes[check_id] = GraphNode(check_id, health_check.title, "health_check")
            module_id = _node_id(f"module:{health_check.module}")
            nodes.setdefault(module_id, GraphNode(module_id, health_check.module, "module"))
            edges.add(GraphEdge(module_id, check_id, "checks", "health"))

        for section in registry.list_report_sections():
            section_id = _node_id(f"report_section:{section.name}")
            nodes[section_id] = GraphNode(section_id, section.title, "report_section")
            nodes.setdefault(_node_id("service:reports"), GraphNode(_node_id("service:reports"), "reports", "service"))
            edges.add(GraphEdge(section_id, _node_id("service:reports"), "renders into", "report"))

        for event_name, handler_count in registry.list_event_handlers().items():
            event_id = _node_id(f"event:{event_name}")
            nodes[event_id] = GraphNode(event_id, f"{event_name} ({handler_count})", "event")

        for port in registry.list_data_ports():
            port_id = _node_id(f"port:{port.module}:{port.direction}:{port.name}")
            nodes[port_id] = GraphNode(port_id, f"{port.direction}: {port.name}", port.kind)
            module_id = _node_id(f"module:{port.module}")
            nodes.setdefault(module_id, GraphNode(module_id, port.module, "module"))
            label = "input" if port.direction == "input" else "output"
            if port.direction == "input":
                edges.add(GraphEdge(port_id, module_id, label, "port"))
            else:
                edges.add(GraphEdge(module_id, port_id, label, "port"))

        for flow in registry.list_flows():
            source_id = _node_id(flow.source)
            target_id = _node_id(flow.target)
            nodes.setdefault(source_id, GraphNode(source_id, flow.source, "flow_endpoint"))
            nodes.setdefault(target_id, GraphNode(target_id, flow.target, "flow_endpoint"))
            edges.add(GraphEdge(source_id, target_id, flow.label, flow.kind))

        return FlowGraph(
            nodes=tuple(sorted(nodes.values(), key=lambda node: node.id)),
            edges=tuple(sorted(edges, key=lambda edge: (edge.kind, edge.source, edge.target, edge.label))),
        )

    def render_mermaid(self) -> str:
        graph = self.build_graph()
        lines = ["flowchart LR"]
        for node in graph.nodes:
            lines.append(f"  {node.id}[\"{_escape_mermaid(node.label)}\"]")
        for edge in graph.edges:
            lines.append(f"  {edge.source} -- \"{_escape_mermaid(edge.label)}\" --> {edge.target}")
        return "\n".join(lines)

    def render_adjacency(self) -> str:
        graph = self.build_graph()
        lines = []
        for edge in graph.edges:
            lines.append(f"{edge.source} -> {edge.target} [{edge.kind}: {edge.label}]")
        return "\n".join(lines)

    def graph_quality_check(self, context: AppContext) -> HealthResult:
        graph = self.build_graph()
        node_ids = {node.id for node in graph.nodes}
        missing = [
            f"{edge.source}->{edge.target}"
            for edge in graph.edges
            if edge.source not in node_ids or edge.target not in node_ids
        ]
        ports = context.registry.list_data_ports()
        modules_with_ports = {port.module for port in ports}
        modules_without_ports = sorted(set(context.registry.list_modules()) - modules_with_ports)
        unhandled_events = []
        handled_events = set(context.registry.list_event_handlers())
        emitted_events = {
            edge.target.removeprefix("event_").replace("_", ".")
            for edge in graph.edges
            if edge.target.startswith("event_")
        }
        for event_name in emitted_events:
            if event_name not in handled_events and "*" not in handled_events:
                unhandled_events.append(event_name)

        if missing:
            return HealthResult("flow_graph.quality", "fail", "Graph edges reference missing nodes: " + ", ".join(missing), "flow_graph")
        if modules_without_ports or unhandled_events:
            details = []
            if modules_without_ports:
                details.append("modules without trace ports: " + ", ".join(modules_without_ports))
            if unhandled_events:
                details.append("unhandled events: " + ", ".join(sorted(unhandled_events)))
            return HealthResult("flow_graph.quality", "warn", " | ".join(details), "flow_graph")
        return HealthResult("flow_graph.quality", "pass", f"Graph has {len(graph.nodes)} nodes and {len(graph.edges)} edges.", "flow_graph")


def _node_id(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]", "_", value).strip("_")


def _escape_mermaid(value: str) -> str:
    return value.replace('"', "'")


def _infer_module_from_title(title: str, modules: dict) -> str | None:
    clean_title = title.lower().replace(" ", "_")
    for module_name in modules:
        if module_name in clean_title or clean_title in module_name:
            return module_name
    return None
