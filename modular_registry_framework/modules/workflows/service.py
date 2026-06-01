from __future__ import annotations

from dataclasses import dataclass

from modular_registry_framework.core.context import AppContext


@dataclass(frozen=True, slots=True)
class WorkflowStep:
    name: str
    module: str
    action: str
    output: str


@dataclass(frozen=True, slots=True)
class WorkflowDefinition:
    name: str
    title: str
    description: str
    steps: tuple[WorkflowStep, ...]


WORKFLOWS = {
    "import_report_export": WorkflowDefinition(
        "import_report_export",
        "Import, Report, Export",
        "Import a file, persist trace/audit events, generate a report, and export a structured result.",
        (
            WorkflowStep("import", "importers", "file.imported", "import result"),
            WorkflowStep("record", "records", "record.created", "record metadata"),
            WorkflowStep("report", "reports", "report.generated", "markdown report"),
            WorkflowStep("export", "exporters", "data.exported", "export artifact"),
        ),
    ),
    "api_sync_review": WorkflowDefinition(
        "api_sync_review",
        "API Sync Review",
        "Check API status, run a sync job, capture raw responses, and summarize health.",
        (
            WorkflowStep("check", "api_clients", "api_clients.available", "client status"),
            WorkflowStep("sync", "jobs", "job.completed", "sync result"),
            WorkflowStep("artifact", "artifact_library", "artifact.created", "raw payload"),
            WorkflowStep("report", "reports", "report.generated", "sync summary"),
        ),
    ),
    "agent_eval": WorkflowDefinition(
        "agent_eval",
        "Agent Evaluation",
        "Run prompts through jobs, trace model decisions, store artifacts, and export scores.",
        (
            WorkflowStep("prompt", "jobs", "job.started", "run id"),
            WorkflowStep("trace", "runtime_trace", "trace event", "event chain"),
            WorkflowStep("artifact", "artifact_library", "artifact.created", "transcript"),
            WorkflowStep("score", "exporters", "data.exported", "score file"),
        ),
    ),
}


class WorkflowService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def list_workflows(self) -> dict[str, WorkflowDefinition]:
        return dict(WORKFLOWS)

    def render(self, name: str | None = None) -> str:
        workflows = [WORKFLOWS[name]] if name else WORKFLOWS.values()
        lines: list[str] = []
        for workflow in workflows:
            lines.extend([f"# {workflow.title}", "", workflow.description, ""])
            for index, step in enumerate(workflow.steps, start=1):
                lines.append(f"{index}. `{step.module}` {step.name}: {step.action} -> {step.output}")
            lines.append("")
        return "\n".join(lines).strip()

    def render_mermaid(self, name: str = "import_report_export") -> str:
        workflow = WORKFLOWS[name]
        lines = ["flowchart LR"]
        for index, step in enumerate(workflow.steps):
            node = _node(index, step)
            lines.append(f'  {node}["{step.module}: {step.name}"]')
            if index:
                previous = _node(index - 1, workflow.steps[index - 1])
                lines.append(f'  {previous} -->|"{workflow.steps[index - 1].output}"| {node}')
        return "\n".join(lines)

    def run_demo(self, name: str = "import_report_export") -> str:
        trace_id = self.context.registry.get_service("runtime_trace").new_trace_id()
        workflow = WORKFLOWS[name]
        for step in workflow.steps:
            self.context.registry.emit(
                f"workflow.{step.name}",
                {
                    "trace_id": trace_id,
                    "workflow": workflow.name,
                    "module": step.module,
                    "action": step.action,
                    "output": step.output,
                },
            )
        self.context.registry.emit("workflow.completed", {"trace_id": trace_id, "workflow": workflow.name})
        return trace_id


def _node(index: int, step: WorkflowStep) -> str:
    return f"{step.module}_{step.name}_{index}".replace("-", "_")

