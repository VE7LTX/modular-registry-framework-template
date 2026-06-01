from __future__ import annotations

from dataclasses import dataclass

from modular_registry_framework.core.context import AppContext


@dataclass(frozen=True, slots=True)
class Recipe:
    name: str
    title: str
    description: str
    workflow: str


RECIPES = {
    "csv_report": Recipe("csv_report", "CSV To Report", "Create a sample CSV, import it, and save a report.", "import_report_export"),
    "api_sync": Recipe("api_sync", "API Sync", "Run the API sync review workflow demo.", "api_sync_review"),
    "agent_eval": Recipe("agent_eval", "Agent Eval", "Run the agent evaluation workflow demo.", "agent_eval"),
}


class RecipeService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def list_recipes(self) -> dict[str, Recipe]:
        return dict(RECIPES)

    def render(self) -> str:
        lines = ["Recipes", "======="]
        for recipe in RECIPES.values():
            lines.append(f"- `{recipe.name}`: {recipe.description}")
        return "\n".join(lines)

    def run(self, name: str = "csv_report") -> str:
        recipe = RECIPES[name]
        trace_id = self.context.registry.get_service("workflows").run_demo(recipe.workflow)
        artifacts = self.context.registry.get_service("artifact_library")
        record = artifacts.create_text_artifact(
            "recipes",
            f"{recipe.name}-{trace_id[:8]}.md",
            f"# {recipe.title}\n\nTrace: `{trace_id}`\n\n{recipe.description}\n",
            trace_id=trace_id,
        )
        self.context.registry.emit(
            "recipe.completed",
            {"trace_id": trace_id, "recipe": recipe.name, "artifact": str(record.path)},
        )
        return str(record.path)

