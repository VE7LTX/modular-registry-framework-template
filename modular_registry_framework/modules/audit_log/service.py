from __future__ import annotations

from .models import AuditEvent


class AuditLogService:
    def __init__(self, max_events: int = 500) -> None:
        self.max_events = max_events
        self._events: list[AuditEvent] = []

    def record(self, event_name: str, payload: dict) -> AuditEvent:
        event = AuditEvent(event_name=event_name, payload=dict(payload))
        self._events.append(event)
        if len(self._events) > self.max_events:
            self._events = self._events[-self.max_events :]
        return event

    def handle_registry_event(self, event: dict) -> None:
        self.record(event["event_name"], event.get("payload", {}))

    def list_events(self, limit: int | None = None) -> list[AuditEvent]:
        events = list(reversed(self._events))
        return events[:limit] if limit else events

