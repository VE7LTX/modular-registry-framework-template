from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_env_secrets_screen
from .service import EnvSecretsService


def register(registry: Registry, context: AppContext) -> None:
    service = EnvSecretsService(context)
    registry.add_module(
        ModuleMetadata(
            name="env_secrets",
            title="Environment And Secrets",
            description="Validates environment variables and redacts secret diagnostics.",
            dependencies=("health_checks",),
        )
    )
    registry.add_service("env_secrets", service)
    registry.add_command("env_secrets.generate_example", service.generate_example)
    registry.add_health_check("env_secrets.required", "Required secrets", service.health_check, "env_secrets")
    registry.add_data_input("env_secrets", ".env file", "file", "Local environment file with key/value pairs.")
    registry.add_data_output("env_secrets", "redacted secret status", "records", "Presence and redacted values only.")
    registry.add_flow("port:env_secrets:input:.env file", "port:env_secrets:output:redacted secret status", "validate secrets")
    registry.add_screen("System", "Secrets", build_env_secrets_screen, order=35)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

