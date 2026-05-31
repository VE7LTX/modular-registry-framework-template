from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GraphNode:
    id: str
    label: str
    kind: str


@dataclass(frozen=True, slots=True)
class GraphEdge:
    source: str
    target: str
    label: str
    kind: str


@dataclass(frozen=True, slots=True)
class FlowGraph:
    nodes: tuple[GraphNode, ...]
    edges: tuple[GraphEdge, ...]

