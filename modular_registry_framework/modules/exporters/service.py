from __future__ import annotations

import csv
import io
import json
from typing import Any
from xml.etree import ElementTree

from modular_registry_framework.core.context import AppContext


class ExportService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def export(self, format_name: str, data: Any) -> str | bytes:
        exporter = self.context.registry.get_exporter(format_name)
        output = exporter.handler(data)
        self.context.registry.emit("data.exported", {"format": exporter.format_name, "extension": exporter.extension})
        return output


def export_json(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True)


def export_jsonl(data: Any) -> str:
    rows = data if isinstance(data, list) else [data]
    return "\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n"


def export_text(data: Any) -> str:
    return str(data)


def export_markdown(data: Any) -> str:
    if isinstance(data, str):
        return data
    return "```json\n" + export_json(data) + "\n```\n"


def export_csv(data: Any) -> str:
    rows = data if isinstance(data, list) else [data]
    output = io.StringIO()
    if not rows:
        return ""
    if not all(isinstance(row, dict) for row in rows):
        rows = [{"value": row} for row in rows]
    fieldnames = sorted({key for row in rows if isinstance(row, dict) for key in row})
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row if isinstance(row, dict) else {"value": row})
    return output.getvalue()


def export_xml(data: Any) -> str:
    root = ElementTree.Element("export")
    root.text = export_json(data)
    tree = ElementTree.ElementTree(root)
    ElementTree.indent(tree, space="  ")
    output = io.BytesIO()
    tree.write(output, encoding="utf-8", xml_declaration=True)
    return output.getvalue().decode("utf-8")


def export_yaml(data: Any) -> str:
    if isinstance(data, dict):
        return "".join(f"{key}: {json.dumps(value, sort_keys=True)}\n" for key, value in sorted(data.items()))
    return f"value: {json.dumps(data, sort_keys=True)}\n"
