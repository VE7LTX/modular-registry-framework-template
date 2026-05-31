from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_reports_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("reports")
    frame = ttk.Frame(parent, padding=16)

    ttk.Label(frame, text="Reports", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    output = tk.Text(frame, height=20, wrap=tk.WORD)
    output.pack(fill=tk.BOTH, expand=True, pady=(12, 8))

    def preview() -> None:
        output.delete("1.0", tk.END)
        output.insert(tk.END, service.render_markdown("Template System Report"))

    def save() -> None:
        record = service.save_markdown("template-system-report.md", "Template System Report")
        output.insert(tk.END, f"\n\nSaved: {record.path}\n")

    controls = ttk.Frame(frame)
    controls.pack(fill=tk.X)
    ttk.Button(controls, text="Preview", command=preview).pack(side=tk.LEFT)
    ttk.Button(controls, text="Save", command=save).pack(side=tk.LEFT, padx=(8, 0))
    preview()
    return frame

