from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_importers_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("importers")
    frame = ttk.Frame(parent, padding=16)

    ttk.Label(frame, text="Importers", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    importers = tk.Listbox(frame, height=8)
    importers.pack(fill=tk.X, pady=(12, 8))
    for extension, importer in context.registry.list_file_importers().items():
        importers.insert(tk.END, f"{extension} | {importer.label} | {importer.description}")

    ttk.Label(frame, text="Recent Imports", font=("Segoe UI", 11, "bold")).pack(anchor=tk.W, pady=(8, 0))
    results = tk.Listbox(frame, height=10)
    results.pack(fill=tk.BOTH, expand=True, pady=(6, 8))

    def refresh() -> None:
        results.delete(0, tk.END)
        for result in service.list_results():
            results.insert(tk.END, f"{result.extension} | {result.path}")

    ttk.Button(frame, text="Refresh", command=refresh).pack(anchor=tk.E)
    refresh()
    return frame

