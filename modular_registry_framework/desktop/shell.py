from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from modular_registry_framework.core.context import AppContext


class DesktopShell:
    """Small Tkinter shell that builds navigation from registered screens."""

    def __init__(self, context: AppContext) -> None:
        self.context = context
        self.root = tk.Tk()
        self.root.title("Modular Registry Framework")
        self.root.geometry("960x640")

        self.nav = ttk.Notebook(self.root)
        self.nav.pack(fill=tk.BOTH, expand=True)
        self._build_registered_screens()

    def _build_registered_screens(self) -> None:
        for screen in self.context.registry.list_screens():
            frame = ttk.Frame(self.nav)
            widget = screen.factory(frame, self.context)
            if widget is not frame:
                widget.pack(fill=tk.BOTH, expand=True)
            self.nav.add(frame, text=f"{screen.area}: {screen.title}")

    def run(self) -> None:
        self.root.mainloop()

