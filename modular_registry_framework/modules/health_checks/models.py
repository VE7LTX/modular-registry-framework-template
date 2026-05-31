from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HealthResult:
    name: str
    status: str
    message: str
    module: str = "system"

