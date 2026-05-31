from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_graph_export_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("graph_export")
    frame = ttk.Frame(parent, padding=16)
    ttk.Label(frame, text="Graph Export", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    output = tk.Text(frame, height=14, wrap=tk.WORD)
    output.pack(fill=tk.BOTH, expand=True, pady=(12, 8))

    def save_mermaid() -> None:
        record = service.save_mermaid()
        output.insert(tk.END, f"Saved Mermaid: {record.path}\n")

    def save_json() -> None:
        record = service.save_json()
        output.insert(tk.END, f"Saved JSON: {record.path}\n")

    controls = ttk.Frame(frame)
    controls.pack(fill=tk.X)
    ttk.Button(controls, text="Save Mermaid", command=save_mermaid).pack(side=tk.LEFT)
    ttk.Button(controls, text="Save JSON", command=save_json).pack(side=tk.LEFT, padx=(8, 0))
    return frame

