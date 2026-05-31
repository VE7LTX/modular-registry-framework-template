from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable

EventHandler = Callable[[dict[str, Any]], Any]
ScreenFactory = Callable[[Any, Any], Any]
CommandHandler = Callable[..., Any]
ImporterHandler = Callable[..., Any]
ReportRenderer = Callable[[Any], str]


@dataclass(frozen=True, slots=True)
class ModuleMetadata:
    name: str
    title: str
    description: str
    version: str = "0.1.0"
    dependencies: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class ScreenRegistration:
    area: str
    title: str
    factory: ScreenFactory
    order: int = 100


@dataclass(frozen=True, slots=True)
class SettingDefinition:
    key: str
    default: Any
    label: str
    help_text: str = ""


@dataclass(frozen=True, slots=True)
class ImporterRegistration:
    extension: str
    handler: ImporterHandler
    label: str
    description: str = ""


@dataclass(frozen=True, slots=True)
class ReportSectionRegistration:
    name: str
    title: str
    renderer: ReportRenderer
    order: int = 100


@dataclass(frozen=True, slots=True)
class DataPortRegistration:
    module: str
    name: str
    direction: str
    kind: str
    description: str = ""


@dataclass(frozen=True, slots=True)
class FlowRegistration:
    source: str
    target: str
    label: str
    kind: str = "data"


class Registry:
    """Directory of capabilities contributed by app modules.

    The registry is intentionally descriptive as well as operational. Modules use
    it to register runtime objects, and the dashboard/flow graph use it to explain
    how the application is assembled.
    """

    def __init__(self) -> None:
        self._modules: dict[str, ModuleMetadata] = {}
        self._services: dict[str, Any] = {}
        self._screens: list[ScreenRegistration] = []
        self._help_topics: dict[str, str] = {}
        self._settings: dict[str, SettingDefinition] = {}
        self._commands: dict[str, CommandHandler] = {}
        self._importers: dict[str, ImporterRegistration] = {}
        self._report_sections: list[ReportSectionRegistration] = []
        self._data_ports: list[DataPortRegistration] = []
        self._flows: list[FlowRegistration] = []
        self._event_handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def add_module(self, metadata: ModuleMetadata) -> None:
        if metadata.name in self._modules:
            raise ValueError(f"Module is already registered: {metadata.name}")
        self._modules[metadata.name] = metadata
        logging.getLogger(__name__).debug("Registered module: %s", metadata)

    def list_modules(self) -> dict[str, ModuleMetadata]:
        return dict(sorted(self._modules.items()))

    def add_service(self, name: str, service: Any) -> None:
        if name in self._services:
            raise ValueError(f"Service is already registered: {name}")
        self._services[name] = service
        logging.getLogger(__name__).debug("Registered service: %s -> %s", name, service.__class__.__name__)

    def get_service(self, name: str) -> Any:
        try:
            return self._services[name]
        except KeyError as exc:
            raise KeyError(f"Unknown service: {name}") from exc

    def list_services(self) -> dict[str, Any]:
        return dict(self._services)

    def add_screen(
        self,
        area: str,
        title: str,
        factory: ScreenFactory,
        order: int = 100,
    ) -> None:
        self._screens.append(ScreenRegistration(area, title, factory, order))
        logging.getLogger(__name__).debug("Registered screen: area=%s title=%s order=%s", area, title, order)

    def list_screens(self) -> list[ScreenRegistration]:
        return sorted(self._screens, key=lambda screen: (screen.area, screen.order, screen.title))

    def add_help_topic(self, key: str, content: str) -> None:
        if key in self._help_topics:
            raise ValueError(f"Help topic is already registered: {key}")
        self._help_topics[key] = content
        logging.getLogger(__name__).debug("Registered help topic: %s", key)

    def get_help_topic(self, key: str) -> str:
        try:
            return self._help_topics[key]
        except KeyError as exc:
            raise KeyError(f"Unknown help topic: {key}") from exc

    def list_help_topics(self) -> dict[str, str]:
        return dict(self._help_topics)

    def add_setting(self, key: str, default: Any, label: str, help_text: str = "") -> None:
        if key in self._settings:
            raise ValueError(f"Setting is already registered: {key}")
        self._settings[key] = SettingDefinition(key, default, label, help_text)
        logging.getLogger(__name__).debug("Registered setting: %s default=%r label=%s", key, default, label)

    def list_settings(self) -> dict[str, SettingDefinition]:
        return dict(self._settings)

    def add_command(self, name: str, handler: CommandHandler) -> None:
        if name in self._commands:
            raise ValueError(f"Command is already registered: {name}")
        self._commands[name] = handler
        logging.getLogger(__name__).debug("Registered command: %s", name)

    def get_command(self, name: str) -> CommandHandler:
        try:
            return self._commands[name]
        except KeyError as exc:
            raise KeyError(f"Unknown command: {name}") from exc

    def list_commands(self) -> dict[str, CommandHandler]:
        return dict(self._commands)

    def add_file_importer(
        self,
        extension: str,
        handler: ImporterHandler,
        label: str | None = None,
        description: str = "",
    ) -> None:
        clean_extension = _normalize_extension(extension)
        if clean_extension in self._importers:
            raise ValueError(f"Importer is already registered: {clean_extension}")
        self._importers[clean_extension] = ImporterRegistration(
            clean_extension,
            handler,
            label or clean_extension.upper(),
            description,
        )
        logging.getLogger(__name__).debug(
            "Registered file importer: extension=%s label=%s", clean_extension, label or clean_extension.upper()
        )

    def get_file_importer(self, extension: str) -> ImporterRegistration:
        clean_extension = _normalize_extension(extension)
        try:
            return self._importers[clean_extension]
        except KeyError as exc:
            raise KeyError(f"Unknown file importer: {clean_extension}") from exc

    def list_file_importers(self) -> dict[str, ImporterRegistration]:
        return dict(sorted(self._importers.items()))

    def add_report_section(
        self,
        name: str,
        title: str,
        renderer: ReportRenderer,
        order: int = 100,
    ) -> None:
        if any(section.name == name for section in self._report_sections):
            raise ValueError(f"Report section is already registered: {name}")
        self._report_sections.append(ReportSectionRegistration(name, title, renderer, order))
        logging.getLogger(__name__).debug("Registered report section: %s title=%s order=%s", name, title, order)

    def list_report_sections(self) -> list[ReportSectionRegistration]:
        return sorted(self._report_sections, key=lambda section: (section.order, section.title))

    def add_data_input(self, module: str, name: str, kind: str, description: str = "") -> None:
        """Declare an input a module consumes so the flow graph can trace it."""
        self._add_data_port(module, name, "input", kind, description)

    def add_data_output(self, module: str, name: str, kind: str, description: str = "") -> None:
        """Declare an output a module produces so the flow graph can trace it."""
        self._add_data_port(module, name, "output", kind, description)

    def _add_data_port(self, module: str, name: str, direction: str, kind: str, description: str = "") -> None:
        port = DataPortRegistration(module, name, direction, kind, description)
        if port in self._data_ports:
            raise ValueError(f"Data port is already registered: {module}.{name}.{direction}")
        self._data_ports.append(port)
        logging.getLogger(__name__).debug("Registered data port: %s", port)

    def list_data_ports(self) -> list[DataPortRegistration]:
        return sorted(self._data_ports, key=lambda port: (port.module, port.direction, port.name))

    def add_flow(self, source: str, target: str, label: str, kind: str = "data") -> None:
        """Declare a directed relationship between two graph endpoints."""
        flow = FlowRegistration(source, target, label, kind)
        if flow in self._flows:
            raise ValueError(f"Flow is already registered: {source} -> {target} ({label})")
        self._flows.append(flow)
        logging.getLogger(__name__).debug("Registered flow: %s", flow)

    def list_flows(self) -> list[FlowRegistration]:
        return sorted(self._flows, key=lambda flow: (flow.kind, flow.source, flow.target, flow.label))

    def on(self, event_name: str, handler: EventHandler) -> None:
        self._event_handlers[event_name].append(handler)
        logging.getLogger(__name__).debug("Registered event handler: %s -> %s", event_name, handler)

    def emit(self, event_name: str, payload: dict[str, Any] | None = None) -> list[Any]:
        event_payload = payload or {}
        logging.getLogger(__name__).debug("Emitting event %s: %s", event_name, event_payload)
        results = [handler(event_payload) for handler in self._event_handlers[event_name]]
        wildcard_payload = {"event_name": event_name, "payload": event_payload}
        results.extend(handler(wildcard_payload) for handler in self._event_handlers["*"])
        return results

    def list_event_handlers(self) -> dict[str, int]:
        return {event_name: len(handlers) for event_name, handlers in sorted(self._event_handlers.items())}


def _normalize_extension(extension: str) -> str:
    clean_extension = extension.strip().lower()
    if not clean_extension:
        raise ValueError("File importer extension cannot be empty.")
    if not clean_extension.startswith("."):
        clean_extension = f".{clean_extension}"
    return clean_extension
