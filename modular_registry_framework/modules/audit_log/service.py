from __future__ import annotations

import json

from modular_registry_framework.core.context import AppContext

from .models import AuditEvent


class AuditLogService:
    def __init__(self, context: AppContext | None = None, max_events: int = 500) -> None:
        self.context = context
        self.max_events = max_events
        self._events: list[AuditEvent] = []

    def record(self, event_name: str, payload: dict) -> AuditEvent:
        event = AuditEvent(event_name=event_name, payload=dict(payload))
        self._events.append(event)
        if len(self._events) > self.max_events:
            self._events = self._events[-self.max_events :]
        self._persist(event)
        return event

    def handle_registry_event(self, event: dict) -> None:
        self.record(event["event_name"], event.get("payload", {}))

    def list_events(self, limit: int | None = None) -> list[AuditEvent]:
        events = list(reversed(self._events))
        return events[:limit] if limit else events

    def _persist(self, event: AuditEvent) -> None:
        if self.context is None or "storage" not in self.context.registry.list_services():
            return
        storage = self.context.registry.get_service("storage")
        try:
            with storage.connect(emit_event=False) as connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS audit_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event_name TEXT NOT NULL,
                        payload_json TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )
                    """
                )
                connection.execute(
                    "INSERT INTO audit_events (event_name, payload_json, created_at) VALUES (?, ?, ?)",
                    (event.event_name, json.dumps(event.payload, sort_keys=True, default=str), event.created_at.isoformat()),
                )
        except Exception:
            return
