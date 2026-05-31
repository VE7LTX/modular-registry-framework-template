from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_storage_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("storage")
    frame = ttk.Frame(parent, padding=16)
    ttk.Label(frame, text="Storage", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    output = tk.Text(frame, height=16, wrap=tk.WORD)
    output.pack(fill=tk.BOTH, expand=True, pady=(12, 8))

    def initialize() -> None:
        service.initialize()
        refresh()

    def refresh() -> None:
        output.delete("1.0", tk.END)
        output.insert(tk.END, f"SQLite path: {service.path}\nExists: {service.path.exists()}\n")

    ttk.Button(frame, text="Initialize", command=initialize).pack(anchor=tk.E)
    refresh()
    return frame

