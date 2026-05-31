from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_api_clients_screen
from .service import ApiClientService, ExampleApiClient


def register(registry: Registry, context: AppContext) -> None:
    service = ApiClientService(context)
    registry.add_module(
        ModuleMetadata(
            name="api_clients",
            title="API Clients",
            description="Registers external API clients with status and health checks.",
            dependencies=("health_checks", "env_secrets", "audit_log"),
        )
    )
    registry.add_service("api_clients", service)
    registry.add_health_check("api_clients.available", "API clients available", service.health_check, "api_clients")
    service.register_client("example", "Example API", ExampleApiClient(), "Local example client for template diagnostics.")
    registry.add_data_input("api_clients", "requests", "api", "Outbound API requests.")
    registry.add_data_output("api_clients", "responses", "api", "API responses and status records.")
    registry.add_flow("port:api_clients:input:requests", "port:api_clients:output:responses", "call API")
    registry.add_screen("Integrations", "API Clients", build_api_clients_screen, order=10)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

