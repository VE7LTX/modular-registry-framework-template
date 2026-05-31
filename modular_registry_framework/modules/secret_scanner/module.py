from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_secret_scanner_screen
from .service import SecretScannerService


def register(registry: Registry, context: AppContext) -> None:
    service = SecretScannerService()
    registry.add_module(
        ModuleMetadata(
            name="secret_scanner",
            title="Secret Scanner",
            description="Scans files for likely hardcoded secrets with redacted output.",
            dependencies=("env_secrets",),
        )
    )
    registry.add_service("secret_scanner", service)
    registry.add_command("secrets.scan", service.scan)
    registry.add_data_input("secret_scanner", "source files", "file", "Project text files.")
    registry.add_data_output("secret_scanner", "redacted findings", "records", "Likely secrets with redacted values.")
    registry.add_flow("port:secret_scanner:input:source files", "port:secret_scanner:output:redacted findings", "scan secrets")
    registry.add_screen("Tools", "Secret Scanner", build_secret_scanner_screen, order=70)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

