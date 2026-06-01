from __future__ import annotations

from collections import defaultdict

from modular_registry_framework.core.context import AppContext


class TraceGraphService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def render_text(self, trace_id: str | None = None) -> str:
        grouped = self._group(trace_id)
        if not grouped:
            return "No traced runtime events yet."
        lines: list[str] = []
        for current_trace_id, events in grouped.items():
            lines.append(f"Trace {current_trace_id}")
            for index, event in enumerate(events, start=1):
                module = event.payload.get("module", _module_from_event(event.event_name))
                output = event.payload.get("output", "")
                lines.append(f"{index}. {module}: {event.event_name}" + (f" -> {output}" if output else ""))
            lines.append("")
        return "\n".join(lines).strip()

    def render_mermaid(self, trace_id: str | None = None) -> str:
        grouped = self._group(trace_id)
        if not grouped:
            return "flowchart LR\n  empty[\"No traced runtime events\"]"
        lines = ["flowchart LR"]
        for group_index, (current_trace_id, events) in enumerate(grouped.items()):
            previous_node = ""
            for index, event in enumerate(events):
                node = f"t{group_index}_{index}"
                label = f"{_short(current_trace_id)} {event.event_name}"
                lines.append(f'  {node}["{label}"]')
                if previous_node:
                    lines.append(f"  {previous_node} --> {node}")
                previous_node = node
        return "\n".join(lines)

    def _group(self, trace_id: str | None) -> dict[str, list]:
        trace = self.context.registry.get_service("runtime_trace")
        grouped: dict[str, list] = defaultdict(list)
        for event in trace.list_events(trace_id):
            grouped[event.trace_id].append(event)
        return dict(grouped)


def _module_from_event(event_name: str) -> str:
    return event_name.split(".", 1)[0]


def _short(trace_id: str) -> str:
    return trace_id[:8]

