from __future__ import annotations

import argparse
import re
from pathlib import Path

MODULE_TEMPLATE_FILES = {
    "__init__.py": """from .module import register

__all__ = ["register"]
""",
    "fields.py": """FIELDS = {{}}
""",
    "help.py": """HELP_TOPICS = {{
    "{module_name}.overview": "{title} module overview."
}}
""",
    "models.py": """from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class {model_name}Item:
    id: int
    name: str
""",
    "service.py": """from __future__ import annotations


class {service_name}Service:
    def list_items(self) -> list[str]:
        return []
""",
    "screens.py": """from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_{module_name}_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("{module_name}")
    frame = ttk.Frame(parent, padding=16)
    ttk.Label(frame, text="{title}", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)

    listbox = tk.Listbox(frame, height=12)
    listbox.pack(fill=tk.BOTH, expand=True, pady=(12, 0))
    for item in service.list_items():
        listbox.insert(tk.END, item)

    return frame
""",
    "module.py": """from __future__ import annotations

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.core.registry import Registry

from .help import HELP_TOPICS
from .screens import build_{module_name}_screen
from .service import {service_name}Service


def register(registry: Registry, context: AppContext) -> None:
    registry.add_service("{module_name}", {service_name}Service())
    registry.add_screen("{area}", "{title}", build_{module_name}_screen, order=100)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)
""",
}


def normalize_module_name(raw_name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9_]+", "_", raw_name.strip().lower())
    name = re.sub(r"_+", "_", name).strip("_")
    if not name:
        raise ValueError("Module name cannot be empty.")
    if name[0].isdigit():
        name = f"module_{name}"
    return name


def pascal_case(raw_name: str) -> str:
    return "".join(part.capitalize() for part in normalize_module_name(raw_name).split("_"))


def create_module(
    modules_dir: Path,
    raw_name: str,
    area: str | None = None,
    title: str | None = None,
    force: bool = False,
) -> Path:
    module_name = normalize_module_name(raw_name)
    module_title = title or pascal_case(module_name)
    module_area = area or module_title
    service_name = pascal_case(module_name)
    target_dir = modules_dir / module_name

    if target_dir.exists() and not force:
        raise FileExistsError(f"Module already exists: {target_dir}")

    target_dir.mkdir(parents=True, exist_ok=True)
    values = {
        "module_name": module_name,
        "title": module_title,
        "area": module_area,
        "service_name": service_name,
        "model_name": service_name,
    }

    for relative_path, template in MODULE_TEMPLATE_FILES.items():
        output_path = target_dir / relative_path
        if output_path.exists() and not force:
            raise FileExistsError(f"File already exists: {output_path}")
        output_path.write_text(template.format(**values), encoding="utf-8")

    return target_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a new modular app feature module.")
    parser.add_argument("name", help="Module name, such as inventory or report_builder.")
    parser.add_argument(
        "--modules-dir",
        default=Path("modular_registry_framework") / "modules",
        type=Path,
        help="Directory where module folders are created.",
    )
    parser.add_argument("--area", help="Navigation area label.")
    parser.add_argument("--title", help="Screen title.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    target = create_module(args.modules_dir, args.name, args.area, args.title, args.force)
    print(f"Created module at {target}")
    print("Add it to modular_registry_framework/modules/__init__.py to enable it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
