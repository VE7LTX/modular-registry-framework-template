from __future__ import annotations

import json
from dataclasses import asdict

from modular_registry_framework.core.context import AppContext


class GraphExportService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def save_mermaid(self, name: str = "system-flow.mmd"):
        flow_graph = self.context.registry.get_service("flow_graph")
        artifacts = self.context.registry.get_service("artifact_library")
        record = artifacts.create_text_artifact("graphs", name, flow_graph.render_mermaid())
        self.context.registry.emit("graph.exported", {"path": str(record.path), "format": "mermaid"})
        return record

    def save_json(self, name: str = "system-flow.json"):
        flow_graph = self.context.registry.get_service("flow_graph")
        graph = flow_graph.build_graph()
        payload = {
            "nodes": [asdict(node) for node in graph.nodes],
            "edges": [asdict(edge) for edge in graph.edges],
        }
        artifacts = self.context.registry.get_service("artifact_library")
        record = artifacts.create_text_artifact("graphs", name, json.dumps(payload, indent=2, sort_keys=True))
        self.context.registry.emit("graph.exported", {"path": str(record.path), "format": "json"})
        return record


def render_graph_export_report(context: AppContext) -> str:
    graph_export = context.registry.get_service("graph_export")
    return "Graph export commands available: `graph_export.save_mermaid`, `graph_export.save_json`."
