from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_command_palette_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("command_palette")
    frame = ttk.Frame(parent, padding=16)
    ttk.Label(frame, text="Command Palette", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    listbox = tk.Listbox(frame, height=22)
    listbox.pack(fill=tk.BOTH, expand=True, pady=(12, 0))
    for command in service.search():
        listbox.insert(tk.END, command.name)
    return frame

