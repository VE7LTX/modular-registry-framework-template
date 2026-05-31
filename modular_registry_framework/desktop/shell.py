from __future__ import annotations

import logging
import traceback
import tkinter as tk
from tkinter import scrolledtext, ttk

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
            logging.getLogger(__name__).debug("Building screen: area=%s title=%s", screen.area, screen.title)
            frame = ttk.Frame(self.nav)
            try:
                widget = screen.factory(frame, self.context)
            except Exception as exc:
                logging.getLogger(__name__).exception("Screen failed to build: %s / %s", screen.area, screen.title)
                self.context.registry.emit(
                    "screen.failed",
                    {"area": screen.area, "title": screen.title, "error": str(exc)},
                )
                widget = self._build_error_screen(frame, screen.title, exc)
            if widget is not frame:
                widget.pack(fill=tk.BOTH, expand=True)
            self.nav.add(frame, text=f"{screen.area}: {screen.title}")

    def _build_error_screen(self, parent: tk.Widget, title: str, error: Exception) -> tk.Widget:
        frame = ttk.Frame(parent, padding=16)
        ttk.Label(frame, text=f"{title} failed to load", font=("Segoe UI", 16, "bold")).pack(anchor=tk.W)
        output = scrolledtext.ScrolledText(frame, height=20, wrap=tk.WORD)
        output.pack(fill=tk.BOTH, expand=True, pady=(12, 0))
        output.insert(tk.END, "".join(traceback.format_exception(error)))
        output.configure(state=tk.DISABLED)
        return frame

    def run(self) -> None:
        self.root.mainloop()
