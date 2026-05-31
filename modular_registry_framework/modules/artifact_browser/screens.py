from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_artifact_browser_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("artifact_browser")
    frame = ttk.Frame(parent, padding=16)
    ttk.Label(frame, text="Artifact Browser", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    output = tk.Text(frame, height=24, wrap=tk.NONE)
    output.pack(fill=tk.BOTH, expand=True, pady=(12, 0))
    output.insert(tk.END, service.render_index())
    return frame

