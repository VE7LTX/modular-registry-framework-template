from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_runtime_trace_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("runtime_trace")
    frame = ttk.Frame(parent, padding=16)
    ttk.Label(frame, text="Runtime Trace", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    output = tk.Text(frame, height=22, wrap=tk.WORD)
    output.pack(fill=tk.BOTH, expand=True, pady=(12, 8))

    def refresh() -> None:
        output.delete("1.0", tk.END)
        output.insert(tk.END, service.render_trace_report())

    ttk.Button(frame, text="Refresh", command=refresh).pack(anchor=tk.E)
    refresh()
    return frame

