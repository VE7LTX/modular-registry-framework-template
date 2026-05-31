from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_flow_graph_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("flow_graph")
    frame = ttk.Frame(parent, padding=16)

    ttk.Label(frame, text="Flow Graph", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    output = tk.Text(frame, height=24, wrap=tk.NONE)
    output.pack(fill=tk.BOTH, expand=True, pady=(12, 8))

    def show_mermaid() -> None:
        output.delete("1.0", tk.END)
        output.insert(tk.END, service.render_mermaid())

    def show_adjacency() -> None:
        output.delete("1.0", tk.END)
        output.insert(tk.END, service.render_adjacency())

    controls = ttk.Frame(frame)
    controls.pack(fill=tk.X)
    ttk.Button(controls, text="Mermaid", command=show_mermaid).pack(side=tk.LEFT)
    ttk.Button(controls, text="Adjacency", command=show_adjacency).pack(side=tk.LEFT, padx=(8, 0))
    show_mermaid()
    return frame

