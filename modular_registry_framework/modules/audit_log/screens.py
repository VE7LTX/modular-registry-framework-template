from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_audit_log_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("audit_log")
    frame = ttk.Frame(parent, padding=16)

    ttk.Label(frame, text="Audit Log", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    listbox = tk.Listbox(frame, height=18)
    listbox.pack(fill=tk.BOTH, expand=True, pady=(12, 8))

    def refresh() -> None:
        listbox.delete(0, tk.END)
        for event in service.list_events(limit=200):
            created = event.created_at.strftime("%Y-%m-%d %H:%M:%S")
            listbox.insert(tk.END, f"{created} UTC | {event.event_name} | {event.payload}")

    ttk.Button(frame, text="Refresh", command=refresh).pack(anchor=tk.E)
    refresh()
    return frame

