from __future__ import annotations

import logging
from pathlib import Path

from modular_registry_framework.core.context import AppContext


class SettingsManagerService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def snapshot(self) -> list[dict]:
        rows = []
        for key, definition in sorted(self.context.registry.list_settings().items()):
            rows.append(
                {
                    "key": key,
                    "value": self.context.settings.get(key, definition.default),
                    "default": definition.default,
                    "label": definition.label,
                    "help_text": definition.help_text,
                }
            )
        return rows

    def set_value(self, key: str, value) -> None:
        if key not in self.context.registry.list_settings():
            raise KeyError(f"Unknown setting: {key}")
        logging.getLogger(__name__).debug("Setting value changed: %s=%r", key, value)
        self.context.settings.set(key, value)
        self.context.registry.emit("setting.changed", {"key": key, "value": value})

    def save(self, path: Path | None = None) -> Path:
        output_path = path or self.context.base_dir / "settings.json"
        logging.getLogger(__name__).debug("Saving settings through settings_manager: %s", output_path)
        self.context.settings.save(output_path)
        self.context.registry.emit("settings.saved", {"path": str(output_path)})
        return output_path
