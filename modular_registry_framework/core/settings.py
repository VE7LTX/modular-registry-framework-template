from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

SUPPORTED_SETTINGS_EXTENSIONS = {".json", ".jsonl", ".xml", ".yaml", ".yml"}


@dataclass(slots=True)
class Settings:
    values: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load(cls, path: Path) -> "Settings":
        if not path.exists():
            return cls()

        extension = _settings_extension(path)
        if extension == ".json":
            with path.open("r", encoding="utf-8") as file:
                return cls(json.load(file))
        if extension == ".jsonl":
            return cls(_load_jsonl(path))
        if extension == ".xml":
            return cls(_load_xml(path))
        if extension in {".yaml", ".yml"}:
            return cls(_load_yaml(path))

        raise ValueError(f"Unsupported settings format: {path.suffix}")

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        extension = _settings_extension(path)

        if extension == ".json":
            with path.open("w", encoding="utf-8") as file:
                json.dump(self.values, file, indent=2, sort_keys=True)
                file.write("\n")
            return
        if extension == ".jsonl":
            _save_jsonl(path, self.values)
            return
        if extension == ".xml":
            _save_xml(path, self.values)
            return
        if extension in {".yaml", ".yml"}:
            _save_yaml(path, self.values)
            return

        raise ValueError(f"Unsupported settings format: {path.suffix}")

    def get(self, key: str, default: Any = None) -> Any:
        return self.values.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.values[key] = value


def _settings_extension(path: Path) -> str:
    extension = path.suffix.lower()
    if extension not in SUPPORTED_SETTINGS_EXTENSIONS:
        raise ValueError(
            "Unsupported settings format "
            f"{extension or '<none>'}. Supported formats: "
            f"{', '.join(sorted(SUPPORTED_SETTINGS_EXTENSIONS))}"
        )
    return extension


def _load_jsonl(path: Path) -> dict[str, Any]:
    values: dict[str, Any] = {}
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            clean_line = line.strip()
            if not clean_line:
                continue
            record = json.loads(clean_line)
            if not isinstance(record, dict):
                raise ValueError(f"JSONL settings line {line_number} must be an object.")

            if set(record) == {"key", "value"}:
                values[str(record["key"])] = record["value"]
                continue
            if len(record) == 1:
                key, value = next(iter(record.items()))
                values[str(key)] = value
                continue

            raise ValueError(
                "JSONL settings lines must be {'key': name, 'value': value} "
                f"or a single-key object. Invalid line: {line_number}"
            )
    return values


def _save_jsonl(path: Path, values: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as file:
        for key in sorted(values):
            record = {"key": key, "value": values[key]}
            file.write(json.dumps(record, sort_keys=True))
            file.write("\n")


def _load_xml(path: Path) -> dict[str, Any]:
    root = ElementTree.parse(path).getroot()
    if root.tag != "settings":
        raise ValueError("XML settings root element must be <settings>.")

    values: dict[str, Any] = {}
    for item in root.findall("setting"):
        key = item.attrib.get("key")
        if not key:
            raise ValueError("XML setting entries require a key attribute.")
        raw_value = item.text or "null"
        values[key] = json.loads(raw_value)
    return values


def _save_xml(path: Path, values: dict[str, Any]) -> None:
    root = ElementTree.Element("settings")
    for key in sorted(values):
        item = ElementTree.SubElement(root, "setting", {"key": key})
        item.text = json.dumps(values[key], sort_keys=True)

    tree = ElementTree.ElementTree(root)
    ElementTree.indent(tree, space="  ")
    tree.write(path, encoding="utf-8", xml_declaration=True)


def _load_yaml(path: Path) -> dict[str, Any]:
    values: dict[str, Any] = {}
    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#"):
                continue
            if ":" not in clean_line:
                raise ValueError(f"YAML settings line {line_number} must be a key/value pair.")

            key, raw_value = clean_line.split(":", 1)
            key = key.strip()
            if not key:
                raise ValueError(f"YAML settings line {line_number} has an empty key.")

            raw_value = raw_value.strip()
            values[key] = _parse_yaml_value(raw_value) if raw_value else None
    return values


def _save_yaml(path: Path, values: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as file:
        for key in sorted(values):
            file.write(f"{key}: {json.dumps(values[key], sort_keys=True)}\n")


def _parse_yaml_value(raw_value: str) -> Any:
    try:
        return json.loads(raw_value)
    except json.JSONDecodeError:
        return raw_value
