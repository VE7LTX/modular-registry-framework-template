from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable

EventHandler = Callable[[dict[str, Any]], Any]
ScreenFactory = Callable[[Any, Any], Any]
CommandHandler = Callable[..., Any]


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


class Registry:
    """Directory of capabilities contributed by app modules."""

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}
        self._screens: list[ScreenRegistration] = []
        self._help_topics: dict[str, str] = {}
        self._settings: dict[str, SettingDefinition] = {}
        self._commands: dict[str, CommandHandler] = {}
        self._event_handlers: dict[str, list[EventHandler]] = defaultdict(list)

    def add_service(self, name: str, service: Any) -> None:
        if name in self._services:
            raise ValueError(f"Service is already registered: {name}")
        self._services[name] = service

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

    def list_screens(self) -> list[ScreenRegistration]:
        return sorted(self._screens, key=lambda screen: (screen.area, screen.order, screen.title))

    def add_help_topic(self, key: str, content: str) -> None:
        if key in self._help_topics:
            raise ValueError(f"Help topic is already registered: {key}")
        self._help_topics[key] = content

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

    def list_settings(self) -> dict[str, SettingDefinition]:
        return dict(self._settings)

    def add_command(self, name: str, handler: CommandHandler) -> None:
        if name in self._commands:
            raise ValueError(f"Command is already registered: {name}")
        self._commands[name] = handler

    def get_command(self, name: str) -> CommandHandler:
        try:
            return self._commands[name]
        except KeyError as exc:
            raise KeyError(f"Unknown command: {name}") from exc

    def on(self, event_name: str, handler: EventHandler) -> None:
        self._event_handlers[event_name].append(handler)

    def emit(self, event_name: str, payload: dict[str, Any] | None = None) -> list[Any]:
        event_payload = payload or {}
        return [handler(event_payload) for handler in self._event_handlers[event_name]]

