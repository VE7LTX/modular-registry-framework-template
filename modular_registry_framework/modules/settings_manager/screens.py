from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_settings_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("settings_manager")
    frame = ttk.Frame(parent, padding=16)

    ttk.Label(frame, text="Settings", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    listbox = tk.Listbox(frame, height=18)
    listbox.pack(fill=tk.BOTH, expand=True, pady=(12, 8))

    def refresh() -> None:
        listbox.delete(0, tk.END)
        for row in service.snapshot():
            listbox.insert(tk.END, f"{row['key']} = {row['value']} | default: {row['default']} | {row['label']}")

    controls = ttk.Frame(frame)
    controls.pack(fill=tk.X)
    ttk.Button(controls, text="Refresh", command=refresh).pack(side=tk.RIGHT)
    ttk.Button(controls, text="Save", command=service.save).pack(side=tk.RIGHT, padx=(0, 8))
    refresh()
    return frame

