from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_importers_screen
from .service import ImportService, load_csv, load_flat_yaml, load_json, load_jsonl, load_text, load_xml


def register(registry: Registry, context: AppContext) -> None:
    registry.add_module(
        ModuleMetadata(
            name="importers",
            title="Importers",
            description="Registers file import handlers and emits file.imported events.",
            dependencies=("audit_log",),
        )
    )
    registry.add_service("importers", ImportService(context))
    registry.add_file_importer(".csv", load_csv, "CSV", "Comma-separated tabular data.")
    registry.add_file_importer(".json", load_json, "JSON", "Structured JSON document.")
    registry.add_file_importer(".jsonl", load_jsonl, "JSONL", "One JSON object per line.")
    registry.add_file_importer(".md", load_text, "Markdown", "Markdown text document.")
    registry.add_file_importer(".txt", load_text, "Text", "Plain text document.")
    registry.add_file_importer(".xml", load_xml, "XML", "XML document summary.")
    registry.add_file_importer(".yaml", load_flat_yaml, "YAML", "Flat YAML mapping.")
    registry.add_file_importer(".yml", load_flat_yaml, "YML", "Flat YAML mapping.")
    registry.add_data_input("importers", "files", "file", "CSV, JSON, JSONL, XML, Markdown, text, YAML, and YML files.")
    registry.add_data_output("importers", "import results", "records", "Parsed file data returned as Python objects.")
    registry.add_flow("port:importers:input:files", "port:importers:output:import results", "parse files", "data")
    registry.add_flow("port:importers:output:import results", "event:file.imported", "emit import event", "event")
    registry.add_screen("Tools", "Importers", build_importers_screen, order=20)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)
