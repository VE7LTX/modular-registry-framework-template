from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


def build_help_screen(parent: tk.Widget, context: AppContext) -> tk.Widget:
    service = context.registry.get_service("help")
    frame = ttk.Frame(parent, padding=16)

    ttk.Label(frame, text="Help", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    body = ttk.Frame(frame)
    body.pack(fill=tk.BOTH, expand=True, pady=(12, 0))

    topics = tk.Listbox(body, width=36)
    topics.pack(side=tk.LEFT, fill=tk.Y)
    output = tk.Text(body, wrap=tk.WORD)
    output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(12, 0))

    topic_map = service.list_topics()
    for key in sorted(topic_map):
        topics.insert(tk.END, key)

    def show_selected(event=None) -> None:
        selection = topics.curselection()
        if not selection:
            return
        key = topics.get(selection[0])
        output.delete("1.0", tk.END)
        output.insert(tk.END, f"{key}\n\n{topic_map[key]}")

    topics.bind("<<ListboxSelect>>", show_selected)
    if topics.size():
        topics.selection_set(0)
        show_selected()
    return frame

