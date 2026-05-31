from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class GenericRecord:
    id: int
    kind: str
    values: dict[str, Any]
    archived: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

