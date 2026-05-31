from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_project_repair_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("project_repair")
    frame = ttk.Frame(parent, padding=16)
    ttk.Label(frame, text="Project Repair", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    output = tk.Text(frame, height=20, wrap=tk.WORD)
    output.pack(fill=tk.BOTH, expand=True, pady=(12, 0))
    output.insert(tk.END, "\n".join(service.plan(context.base_dir)))
    return frame

