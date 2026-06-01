from __future__ import annotations

from dataclasses import dataclass

from modular_registry_framework.core.context import AppContext


@dataclass(frozen=True, slots=True)
class SurfaceMap:
    name: str
    cli: tuple[str, ...] = ()
    screens: tuple[str, ...] = ()
    reports: tuple[str, ...] = ()
    dashboard: bool = False


class UiAdapterService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def list_surfaces(self) -> list[SurfaceMap]:
        modules = self.context.registry.list_modules()
        commands = sorted(self.context.registry.list_commands())
        screens = self.context.registry.list_screens()
        reports = self.context.registry.list_report_sections()
        surfaces: list[SurfaceMap] = []
        for name in sorted(modules):
            surfaces.append(
                SurfaceMap(
                    name=name,
                    cli=tuple(command for command in commands if command.startswith(f"{name}.") or command.startswith(f"{name}_")),
                    screens=tuple(f"{screen.area} / {screen.title}" for screen in screens if _matches(name, screen.title)),
                    reports=tuple(section.name for section in reports if section.name.startswith(name) or section.name.startswith(f"{name}.")),
                    dashboard=name in {"dashboard", "health_checks", "runtime_trace", "flow_graph"},
                )
            )
        return surfaces

    def coverage_summary(self) -> dict[str, int]:
        surfaces = self.list_surfaces()
        return {
            "modules": len(surfaces),
            "with_cli": sum(1 for surface in surfaces if surface.cli),
            "with_screens": sum(1 for surface in surfaces if surface.screens),
            "with_reports": sum(1 for surface in surfaces if surface.reports),
        }

    def render_text(self) -> str:
        lines = ["UI Adapter Coverage", "===================", "Module | CLI | Screens | Reports | Dashboard"]
        lines.append("--- | --- | --- | --- | ---")
        for surface in self.list_surfaces():
            lines.append(
                f"{surface.name} | {len(surface.cli)} | {len(surface.screens)} | "
                f"{len(surface.reports)} | {'yes' if surface.dashboard else 'no'}"
            )
        return "\n".join(lines)


def _matches(module_name: str, title: str) -> bool:
    normalized_title = title.lower().replace(" ", "_")
    return module_name in normalized_title or normalized_title in module_name

