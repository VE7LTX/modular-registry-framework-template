from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ApiStatus:
    name: str
    label: str
    available: bool
    message: str

