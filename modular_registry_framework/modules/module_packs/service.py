from __future__ import annotations

from dataclasses import dataclass

from modular_registry_framework.modules.template_generator.service import APP_TEMPLATES


@dataclass(frozen=True, slots=True)
class ModulePack:
    name: str
    modules: tuple[str, ...]


class ModulePackService:
    def list_packs(self) -> dict[str, ModulePack]:
        return {
            name: ModulePack(name, template.modules)
            for name, template in APP_TEMPLATES.items()
        }

    def render_markdown(self) -> str:
        lines = ["# Module Packs", ""]
        for pack in self.list_packs().values():
            lines.append(f"## {pack.name}")
            lines.append("")
            for module in pack.modules:
                lines.append(f"- `{module}`")
            lines.append("")
        return "\n".join(lines)

