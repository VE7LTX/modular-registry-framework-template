from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_exporters_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    frame = ttk.Frame(parent, padding=16)
    ttk.Label(frame, text="Exporters", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    listbox = tk.Listbox(frame, height=18)
    listbox.pack(fill=tk.BOTH, expand=True, pady=(12, 8))
    for name, exporter in context.registry.list_exporters().items():
        listbox.insert(tk.END, f"{name} | {exporter.extension} | {exporter.description}")
    return frame

