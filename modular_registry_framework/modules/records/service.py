from __future__ import annotations

from typing import Any

from modular_registry_framework.core.context import AppContext

from .models import GenericRecord


class RecordService:
    def __init__(self, context: AppContext) -> None:
        self.context = context
        self._next_id = 1
        self._records: dict[int, GenericRecord] = {}

    def create(self, kind: str, values: dict[str, Any]) -> GenericRecord:
        if not kind.strip():
            raise ValueError("Record kind is required.")
        record = GenericRecord(self._next_id, kind.strip(), dict(values))
        self._next_id += 1
        self._records[record.id] = record
        self.context.registry.emit("record.created", {"id": record.id, "kind": record.kind})
        return record

    def list_records(self, kind: str | None = None, include_archived: bool = False) -> list[GenericRecord]:
        records = list(self._records.values())
        if kind is not None:
            records = [record for record in records if record.kind == kind]
        if not include_archived:
            records = [record for record in records if not record.archived]
        return sorted(records, key=lambda record: record.id)

    def archive(self, record_id: int) -> GenericRecord:
        record = self._records[record_id]
        archived = GenericRecord(record.id, record.kind, record.values, True, record.created_at)
        self._records[record_id] = archived
        self.context.registry.emit("record.archived", {"id": archived.id, "kind": archived.kind})
        return archived

