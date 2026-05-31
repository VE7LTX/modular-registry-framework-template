from __future__ import annotations

import logging

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.logging_config import configure_logging


class DiagnosticsService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def snapshot(self) -> dict:
        root = logging.getLogger()
        return {
            "debug_enabled": self.context.settings.get("debug.enabled", False),
            "logging_level": logging.getLevelName(root.level),
            "handlers": [handler.__class__.__name__ for handler in root.handlers],
            "handler_count": len(root.handlers),
            "event_handlers": self.context.registry.list_event_handlers(),
        }

    def set_debug_enabled(self, enabled: bool) -> None:
        logging.getLogger(__name__).debug("Setting debug mode: %s", enabled)
        self.context.settings.set("debug.enabled", enabled)
        self.context.settings.set("logging.level", "DEBUG" if enabled else "INFO")
        self.context.settings.set("logging.file_enabled", enabled)
        configure_logging(self.context.settings, self.context.base_dir)
        self.context.registry.emit("diagnostics.debug_changed", {"enabled": enabled})

    def set_logging_level(self, level: str) -> None:
        clean_level = level.upper()
        if clean_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError(f"Unsupported logging level: {level}")
        logging.getLogger(__name__).debug("Setting logging level: %s", clean_level)
        self.context.settings.set("logging.level", clean_level)
        configure_logging(self.context.settings, self.context.base_dir)
        self.context.registry.emit("diagnostics.logging_level_changed", {"level": clean_level})
