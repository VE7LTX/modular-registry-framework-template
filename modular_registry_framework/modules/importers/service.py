from __future__ import annotations

import csv
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from modular_registry_framework.core.context import AppContext


@dataclass(frozen=True, slots=True)
class ImportResult:
    path: Path
    extension: str
    data: Any


class ImportService:
    def __init__(self, context: AppContext) -> None:
        self.context = context
        self._results: list[ImportResult] = []

    def import_file(self, path: Path) -> ImportResult:
        logger = logging.getLogger(__name__)
        logger.debug("Import requested: path=%s suffix=%s", path, path.suffix)
        importer = self.context.registry.get_file_importer(path.suffix)
        data = importer.handler(path, self.context)
        result = ImportResult(path=path, extension=importer.extension, data=data)
        self._results.append(result)
        logger.debug("Import completed: path=%s extension=%s data_type=%s", path, importer.extension, type(data).__name__)
        self.context.registry.emit(
            "file.imported",
            {"path": str(path), "extension": importer.extension, "label": importer.label},
        )
        return result

    def list_results(self) -> list[ImportResult]:
        return list(reversed(self._results))


def load_csv(path: Path, context: AppContext) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def load_json(path: Path, context: AppContext) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_jsonl(path: Path, context: AppContext) -> list[Any]:
    with path.open("r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def load_text(path: Path, context: AppContext) -> str:
    return path.read_text(encoding="utf-8")


def load_xml(path: Path, context: AppContext) -> dict:
    root = ElementTree.parse(path).getroot()
    return {
        "tag": root.tag,
        "attributes": dict(root.attrib),
        "text": root.text.strip() if root.text else "",
        "children": [child.tag for child in root],
    }


def load_flat_yaml(path: Path, context: AppContext) -> dict[str, Any]:
    values: dict[str, Any] = {}
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue
            key, raw_value = clean_line.split(":", 1)
            values[key.strip()] = _parse_scalar(raw_value.strip())
    return values


def _parse_scalar(value: str) -> Any:
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value
