from __future__ import annotations

import logging
from typing import Any

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.modules.health_checks.models import HealthResult

from .models import ApiStatus


class ApiClientService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def register_client(self, name: str, label: str, client: Any, description: str = "") -> None:
        self.context.registry.add_api_client(name, label, client, description)
        self.context.registry.emit("api.client_registered", {"name": name, "label": label})

    def status_all(self) -> list[ApiStatus]:
        statuses: list[ApiStatus] = []
        for registration in self.context.registry.list_api_clients().values():
            client = registration.client
            try:
                if hasattr(client, "health_check"):
                    result = client.health_check()
                    available = bool(result.get("available", True)) if isinstance(result, dict) else bool(result)
                    message = result.get("message", "ok") if isinstance(result, dict) else "ok"
                else:
                    available = True
                    message = "registered"
            except Exception as exc:
                logging.getLogger(__name__).exception("API client health check failed: %s", registration.name)
                available = False
                message = str(exc)
            statuses.append(ApiStatus(registration.name, registration.label, available, message))
        return statuses

    def health_check(self, context: AppContext) -> HealthResult:
        statuses = self.status_all()
        failed = [status.name for status in statuses if not status.available]
        if failed:
            return HealthResult("api_clients.available", "fail", f"Unavailable API clients: {', '.join(failed)}", "api_clients")
        return HealthResult("api_clients.available", "pass", f"{len(statuses)} API clients registered.", "api_clients")


class ExampleApiClient:
    def health_check(self) -> dict:
        return {"available": True, "message": "Example API client is local-only and available."}

