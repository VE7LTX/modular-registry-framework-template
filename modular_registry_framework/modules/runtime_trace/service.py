from __future__ import annotations

from uuid import uuid4

from .models import TraceEvent


class RuntimeTraceService:
    def __init__(self) -> None:
        self._events: list[TraceEvent] = []

    def new_trace_id(self) -> str:
        return uuid4().hex

    def handle_registry_event(self, event: dict) -> None:
        payload = event.get("payload", {})
        trace_id = payload.get("trace_id")
        if trace_id:
            self._events.append(TraceEvent(trace_id, event["event_name"], dict(payload)))

    def list_events(self, trace_id: str | None = None) -> list[TraceEvent]:
        events = list(self._events)
        if trace_id:
            events = [event for event in events if event.trace_id == trace_id]
        return events

    def render_trace_report(self) -> str:
        lines = []
        for event in self.list_events():
            lines.append(f"- `{event.trace_id}` {event.event_name}: {event.payload}")
        return "\n".join(lines) if lines else "No traced events yet."

