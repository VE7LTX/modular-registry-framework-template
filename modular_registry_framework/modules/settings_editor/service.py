from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from modular_registry_framework.core.context import AppContext


class SettingsEditorService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def set_from_text(self, key: str, raw_value: str) -> Any:
        if key not in self.context.registry.list_settings():
            raise KeyError(f"Unknown setting: {key}")
        try:
            value = json.loads(raw_value)
        except json.JSONDecodeError:
            value = raw_value
        self.context.settings.set(key, value)
        self.context.registry.emit("setting.changed", {"key": key, "value": value})
        return value

    def save(self, path: Path | None = None) -> Path:
        output_path = path or self.context.base_dir / "settings.json"
        self.context.settings.save(output_path)
        self.context.registry.emit("settings.saved", {"path": str(output_path)})
        return output_path

    def render_text(self) -> str:
        rows = []
        for key, setting in self.context.registry.list_settings().items():
            rows.append(f"{key} = {self.context.settings.get(key, setting.default)!r} # {setting.label}")
        return "\n".join(rows)

