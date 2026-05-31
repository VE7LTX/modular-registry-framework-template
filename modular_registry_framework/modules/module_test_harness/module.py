from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_module_test_harness_screen
from .service import ModuleTestHarnessService


def register(registry: Registry, context: AppContext) -> None:
    service = ModuleTestHarnessService()
    registry.add_module(
        ModuleMetadata(
            name="module_test_harness",
            title="Module Test Harness",
            description="Generates baseline tests for module registration and traceability.",
            dependencies=("template_generator",),
        )
    )
    registry.add_service("module_test_harness", service)
    registry.add_command("module_test.render", service.render_registration_test)
    registry.add_command("module_test.write", service.write_registration_test)
    registry.add_data_input("module_test_harness", "module name", "user_input", "Module name to generate tests for.")
    registry.add_data_output("module_test_harness", "pytest file", "file", "Generated pytest module smoke test.")
    registry.add_flow("port:module_test_harness:input:module name", "port:module_test_harness:output:pytest file", "generate tests")
    registry.add_screen("Tools", "Module Test Harness", build_module_test_harness_screen, order=80)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

