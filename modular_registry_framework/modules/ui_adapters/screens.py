from __future__ import annotations

import tkinter as tk
from tkinter import scrolledtext, ttk


def build_ui_adapters_screen(parent: tk.Widget, context) -> tk.Widget:
    frame = ttk.Frame(parent, padding=12)
    ttk.Label(frame, text="UI Adapters", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
    text = scrolledtext.ScrolledText(frame, height=22, wrap=tk.WORD)
    text.pack(fill=tk.BOTH, expand=True)
    text.insert(tk.END, context.registry.get_service("ui_adapters").render_text())
    text.configure(state=tk.DISABLED)
    return frame

