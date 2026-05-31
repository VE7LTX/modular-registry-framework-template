from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_artifact_library_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("artifact_library")
    frame = ttk.Frame(parent, padding=16)

    ttk.Label(frame, text="Artifact Library", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    listbox = tk.Listbox(frame, height=18)
    listbox.pack(fill=tk.BOTH, expand=True, pady=(12, 8))

    def refresh() -> None:
        listbox.delete(0, tk.END)
        for artifact in service.list_artifacts():
            listbox.insert(tk.END, f"{artifact.kind} | {artifact.name} | {artifact.path}")

    ttk.Button(frame, text="Refresh", command=refresh).pack(anchor=tk.E)
    refresh()
    return frame

