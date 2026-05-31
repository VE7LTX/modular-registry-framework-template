from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .registry import Registry
from .settings import Settings


@dataclass(slots=True)
class AppContext:
    db: Any
    settings: Settings
    registry: Registry
    base_dir: Path

