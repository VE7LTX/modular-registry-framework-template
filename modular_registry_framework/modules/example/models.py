from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExampleItem:
    id: int
    name: str
    status: str = "New"

