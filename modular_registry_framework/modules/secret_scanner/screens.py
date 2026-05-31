from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_secret_scanner_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("secret_scanner")
    frame = ttk.Frame(parent, padding=16)
    ttk.Label(frame, text="Secret Scanner", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    output = tk.Text(frame, height=22, wrap=tk.WORD)
    output.pack(fill=tk.BOTH, expand=True, pady=(12, 8))

    def scan() -> None:
        output.delete("1.0", tk.END)
        output.insert(tk.END, service.render_markdown(service.scan(context.base_dir)))

    ttk.Button(frame, text="Scan Current Project", command=scan).pack(anchor=tk.E)
    return frame

