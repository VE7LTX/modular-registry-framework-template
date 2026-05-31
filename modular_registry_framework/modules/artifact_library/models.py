from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ArtifactRecord:
    kind: str
    name: str
    path: Path
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

