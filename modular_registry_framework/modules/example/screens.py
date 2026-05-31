from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from modular_registry_framework.core.context import AppContext


def build_example_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("example")
    frame = ttk.Frame(parent, padding=16)

    title = ttk.Label(frame, text="Example Module", font=("Segoe UI", 16, "bold"))
    title.pack(anchor=tk.W)

    listbox = tk.Listbox(frame, height=12)
    listbox.pack(fill=tk.BOTH, expand=True, pady=(12, 8))

    entry = ttk.Entry(frame)
    entry.pack(fill=tk.X)

    def refresh() -> None:
        listbox.delete(0, tk.END)
        for item in service.list_items():
            listbox.insert(tk.END, f"{item.id}: {item.name} [{item.status}]")

    def add_item() -> None:
        try:
            service.create_item(entry.get())
        except ValueError as exc:
            messagebox.showerror("Cannot add item", str(exc))
            return
        entry.delete(0, tk.END)
        refresh()

    button = ttk.Button(frame, text="Add Item", command=add_item)
    button.pack(anchor=tk.E, pady=(8, 0))

    refresh()
    return frame

