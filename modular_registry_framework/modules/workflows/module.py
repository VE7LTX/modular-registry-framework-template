from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_workflows_screen
from .service import WorkflowService


def register(registry: Registry, context: AppContext) -> None:
    service = WorkflowService(context)
    registry.add_module(
        ModuleMetadata(
            name="workflows",
            title="Workflows",
            description="Defines repeatable module pipelines for common app operations.",
            dependencies=("runtime_trace", "jobs", "importers", "reports", "exporters"),
        )
    )
    registry.add_service("workflows", service)
    registry.add_command("workflows.render", service.render)
    registry.add_command("workflows.mermaid", service.render_mermaid)
    registry.add_command("workflows.demo", service.run_demo)
    registry.add_data_input("workflows", "workflow definition", "metadata", "Named pipeline steps.")
    registry.add_data_output("workflows", "workflow run", "event", "Traceable workflow events.")
    registry.add_flow("port:workflows:input:workflow definition", "port:workflows:output:workflow run", "execute pipeline")
    registry.add_screen("Tools", "Workflows", build_workflows_screen, order=15)
    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)

