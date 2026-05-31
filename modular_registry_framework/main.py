from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.logging_config import configure_logging
from modular_registry_framework.core.registry import Registry
from modular_registry_framework.core.settings import Settings
from modular_registry_framework.desktop.shell import DesktopShell
from modular_registry_framework.modules import MODULES


class NullDatabase:
    """Placeholder database object for the template app."""

    def close(self) -> None:
        return None


def build_context(base_dir: Path | None = None, db: Any | None = None) -> AppContext:
    base = base_dir or Path.cwd()
    registry = Registry()
    settings = Settings.load(base / "settings.json")
    configure_logging(settings, base)
    logger = logging.getLogger(__name__)
    logger.debug("Building app context with base_dir=%s", base)
    context = AppContext(
        db=db or NullDatabase(),
        settings=settings,
        registry=registry,
        base_dir=base,
    )

    for module in MODULES:
        logger.debug("Registering module entry point: %s", module.__name__)
        module.register(registry, context)
    logger.debug(
        "Context built: modules=%s services=%s screens=%s",
        list(registry.list_modules()),
        list(registry.list_services()),
        len(registry.list_screens()),
    )

    return context


def main() -> int:
    context = build_context()
    app = DesktopShell(context)
    context.registry.emit("app.started", {"context": context})
    app.run()
    context.registry.emit("app.shutdown", {"context": context})
    context.db.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
