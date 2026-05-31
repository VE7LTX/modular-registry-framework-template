from __future__ import annotations

import logging
from pathlib import Path

from modular_registry_framework.core.context import AppContext

from .models import ArtifactRecord


class ArtifactLibraryService:
    def __init__(self, context: AppContext, root_name: str = "artifacts") -> None:
        self.context = context
        self.root = context.base_dir / root_name
        self._records: list[ArtifactRecord] = []

    def ensure_kind(self, kind: str) -> Path:
        path = self.root / _safe_path_name(kind)
        path.mkdir(parents=True, exist_ok=True)
        logging.getLogger(__name__).debug("Ensured artifact folder: kind=%s path=%s", kind, path)
        return path

    def create_text_artifact(self, kind: str, name: str, content: str) -> ArtifactRecord:
        logging.getLogger(__name__).debug("Creating text artifact: kind=%s name=%s bytes=%s", kind, name, len(content))
        folder = self.ensure_kind(kind)
        path = folder / _safe_path_name(name)
        path.write_text(content, encoding="utf-8")
        record = ArtifactRecord(kind=kind, name=name, path=path)
        self._records.append(record)
        self.context.registry.emit(
            "artifact.created",
            {"kind": record.kind, "name": record.name, "path": str(record.path)},
        )
        return record

    def register_external_artifact(self, kind: str, name: str, path: Path) -> ArtifactRecord:
        logging.getLogger(__name__).debug("Registering external artifact: kind=%s name=%s path=%s", kind, name, path)
        record = ArtifactRecord(kind=kind, name=name, path=path)
        self._records.append(record)
        self.context.registry.emit(
            "artifact.registered",
            {"kind": record.kind, "name": record.name, "path": str(record.path)},
        )
        return record

    def list_artifacts(self) -> list[ArtifactRecord]:
        return list(reversed(self._records))


def _safe_path_name(value: str) -> str:
    return "".join(character if character.isalnum() or character in "._-" else "_" for character in value.strip())
