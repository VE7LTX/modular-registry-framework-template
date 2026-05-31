from __future__ import annotations

import json
from uuid import uuid4

from modular_registry_framework.core.context import AppContext

from .models import TraceEvent


class RuntimeTraceService:
    def __init__(self, context: AppContext | None = None) -> None:
        self.context = context
        self._events: list[TraceEvent] = []

    def new_trace_id(self) -> str:
        return uuid4().hex

    def handle_registry_event(self, event: dict) -> None:
        payload = event.get("payload", {})
        trace_id = payload.get("trace_id")
        if trace_id:
            trace_event = TraceEvent(trace_id, event["event_name"], dict(payload))
            self._events.append(trace_event)
            self._persist(trace_event)

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

    def _persist(self, event: TraceEvent) -> None:
        if self.context is None or "storage" not in self.context.registry.list_services():
            return
        storage = self.context.registry.get_service("storage")
        try:
            with storage.connect(emit_event=False) as connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS trace_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        trace_id TEXT NOT NULL,
                        event_name TEXT NOT NULL,
                        payload_json TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )
                    """
                )
                connection.execute(
                    "INSERT INTO trace_events (trace_id, event_name, payload_json, created_at) VALUES (?, ?, ?, ?)",
                    (
                        event.trace_id,
                        event.event_name,
                        json.dumps(event.payload, sort_keys=True, default=str),
                        event.created_at.isoformat(),
                    ),
                )
        except Exception:
            return
