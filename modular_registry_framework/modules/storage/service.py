from __future__ import annotations

import shutil
import sqlite3
from pathlib import Path

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.modules.health_checks.models import HealthResult


class AutoClosingConnection(sqlite3.Connection):
    def __exit__(self, exc_type, exc_value, traceback) -> bool:
        try:
            return super().__exit__(exc_type, exc_value, traceback)
        finally:
            self.close()


class StorageService:
    def __init__(self, context: AppContext, relative_path: str = "data/app.sqlite3") -> None:
        self.context = context
        self.path = context.base_dir / relative_path

    def connect(self, emit_event: bool = True) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path, factory=AutoClosingConnection)
        connection.execute("PRAGMA temp_store = MEMORY")
        connection.execute("PRAGMA journal_mode = MEMORY")
        if emit_event:
            self.context.registry.emit("storage.opened", {"path": str(self.path)})
        return connection

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.execute(
                "CREATE TABLE IF NOT EXISTS app_metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
            )
            connection.execute(
                "INSERT OR REPLACE INTO app_metadata (key, value) VALUES ('schema_version', '1')"
            )
        self.context.registry.emit("storage.initialized", {"path": str(self.path)})

    def backup(self, name: str = "app.sqlite3.bak") -> Path:
        self.initialize()
        backup_path = self.context.base_dir / "artifacts" / "backups" / name
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.path, backup_path)
        self.context.registry.emit("storage.backed_up", {"path": str(backup_path)})
        return backup_path

    def health_check(self, context: AppContext) -> HealthResult:
        try:
            self.initialize()
        except Exception as exc:
            return HealthResult("storage.sqlite", "fail", str(exc), "storage")
        return HealthResult("storage.sqlite", "pass", f"SQLite ready at {self.path}.", "storage")


def render_storage_report(context: AppContext) -> str:
    storage = context.registry.get_service("storage")
    return f"- SQLite path: `{storage.path}`\n- Exists: {storage.path.exists()}"
