from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_exporters_screen
from .service import (
    ExportService,
    export_csv,
    export_json,
    export_jsonl,
    export_markdown,
    export_text,
    export_xml,
    export_yaml,
)


def register(registry: Registry, context: AppContext) -> None:
    service = ExportService(context)
    registry.add_module(
        ModuleMetadata(
            name="exporters",
            title="Exporters",
            description="Registers reusable output format handlers.",
            dependencies=("artifact_library",),
        )
    )
    registry.add_service("exporters", service)
    registry.add_command("exporters.export", service.export)
    registry.add_command("exporters.export_artifact", service.export_artifact)
    registry.add_exporter("json", ".json", export_json, "JSON", "Pretty JSON document.")
    registry.add_exporter("jsonl", ".jsonl", export_jsonl, "JSONL", "One JSON object per line.")
    registry.add_exporter("txt", ".txt", export_text, "Text", "Plain text output.")
    registry.add_exporter("md", ".md", export_markdown, "Markdown", "Markdown output.")
    registry.add_exporter("csv", ".csv", export_csv, "CSV", "Comma-separated values.")
    registry.add_exporter("xml", ".xml", export_xml, "XML", "XML wrapper with JSON text payload.")
    registry.add_exporter("yaml", ".yaml", export_yaml, "YAML", "Flat YAML-style mapping.")
    registry.add_exporter("yml", ".yml", export_yaml, "YML", "Flat YAML-style mapping.")
    registry.add_data_input("exporters", "structured data", "records", "Data from records, reports, traces, or imports.")
    registry.add_data_output("exporters", "export text", "file", "Serialized export payload.")
    registry.add_flow("port:exporters:input:structured data", "port:exporters:output:export text", "serialize data")
    registry.add_flow("port:exporters:output:export text", "event:data.exported", "emit export event", "event")
    registry.add_screen("Tools", "Exporters", build_exporters_screen, order=40)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)
