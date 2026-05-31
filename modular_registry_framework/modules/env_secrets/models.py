from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SecretRequirement:
    key: str
    label: str
    required: bool = True

