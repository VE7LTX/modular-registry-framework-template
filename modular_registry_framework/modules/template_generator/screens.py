from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_template_generator_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("template_generator")
    frame = ttk.Frame(parent, padding=16)
    ttk.Label(frame, text="Template Generator", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    listbox = tk.Listbox(frame, height=16)
    listbox.pack(fill=tk.BOTH, expand=True, pady=(12, 8))
    for template in service.list_templates().values():
        listbox.insert(tk.END, f"{template.name} | {template.description}")
    return frame

