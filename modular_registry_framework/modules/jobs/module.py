from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import ModuleMetadata, Registry

from .help import HELP_TOPICS
from .screens import build_jobs_screen
from .service import JobService


def register(registry: Registry, context: AppContext) -> None:
    registry.add_module(
        ModuleMetadata(
            name="jobs",
            title="Jobs",
            description="Provides a common lifecycle for imports, scans, reports, and syncs.",
            dependencies=("audit_log",),
        )
    )
    registry.add_service("jobs", JobService(context))
    registry.add_data_input("jobs", "callable work", "task", "Long-running or important unit of work.")
    registry.add_data_output("jobs", "job records", "records", "Started, completed, or failed job records.")
    registry.add_flow("port:jobs:input:callable work", "port:jobs:output:job records", "run job", "data")
    registry.add_flow("port:jobs:output:job records", "event:job.completed", "emit completion event", "event")
    registry.add_screen("System", "Jobs", build_jobs_screen, order=60)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)
