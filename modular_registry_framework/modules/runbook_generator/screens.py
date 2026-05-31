from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_runbook_generator_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("runbook_generator")
    frame = ttk.Frame(parent, padding=16)
    ttk.Label(frame, text="Runbook Generator", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    output = tk.Text(frame, height=24, wrap=tk.WORD)
    output.pack(fill=tk.BOTH, expand=True, pady=(12, 8))
    output.insert(tk.END, service.render_markdown())
    return frame

