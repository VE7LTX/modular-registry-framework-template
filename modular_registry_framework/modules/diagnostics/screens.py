from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_diagnostics_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("diagnostics")
    frame = ttk.Frame(parent, padding=16)

    ttk.Label(frame, text="Diagnostics", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)

    debug_enabled = tk.BooleanVar(value=bool(context.settings.get("debug.enabled", False)))
    level_value = tk.StringVar(value=str(context.settings.get("logging.level", "INFO")).upper())
    output = tk.Text(frame, height=16, wrap=tk.WORD)

    def refresh() -> None:
        output.delete("1.0", tk.END)
        for key, value in service.snapshot().items():
            output.insert(tk.END, f"{key}: {value}\n")

    def apply_debug() -> None:
        service.set_debug_enabled(debug_enabled.get())
        level_value.set(str(context.settings.get("logging.level", "INFO")).upper())
        refresh()

    def apply_level() -> None:
        service.set_logging_level(level_value.get())
        refresh()

    controls = ttk.Frame(frame)
    controls.pack(fill=tk.X, pady=(12, 8))
    ttk.Checkbutton(controls, text="Debug mode", variable=debug_enabled, command=apply_debug).pack(side=tk.LEFT)
    ttk.Combobox(
        controls,
        textvariable=level_value,
        values=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
        width=12,
        state="readonly",
    ).pack(side=tk.LEFT, padx=(12, 4))
    ttk.Button(controls, text="Apply Level", command=apply_level).pack(side=tk.LEFT)
    ttk.Button(controls, text="Refresh", command=refresh).pack(side=tk.RIGHT)

    output.pack(fill=tk.BOTH, expand=True)
    refresh()
    return frame

