from __future__ import annotations

import logging
from pathlib import Path

from .settings import Settings

DEFAULT_LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def configure_logging(settings: Settings, base_dir: Path) -> None:
    debug_enabled = bool(settings.get("debug.enabled", False))
    level_name = str(settings.get("logging.level", "DEBUG" if debug_enabled else "INFO")).upper()
    level = getattr(logging, level_name, logging.INFO)
    console_enabled = bool(settings.get("logging.console_enabled", True))
    file_enabled = bool(settings.get("logging.file_enabled", debug_enabled))
    log_file = Path(str(settings.get("logging.file", "logs/app.log")))
    if not log_file.is_absolute():
        log_file = base_dir / log_file

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)

    formatter = logging.Formatter(DEFAULT_LOG_FORMAT)
    if console_enabled:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)
        root.addHandler(console_handler)

    if file_enabled:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        root.addHandler(file_handler)

    logging.getLogger(__name__).debug(
        "Logging configured: debug=%s level=%s console=%s file=%s",
        debug_enabled,
        level_name,
        console_enabled,
        str(log_file) if file_enabled else None,
    )

