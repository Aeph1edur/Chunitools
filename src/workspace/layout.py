"""Type-checking stub — re-exports MainWindow from the actual location.

Used by ``from src.workspace.layout import MainWindow`` under TYPE_CHECKING
guards across the codebase.  At runtime the import never executes.
"""

from __future__ import annotations

from src.ui.window.window import MainWindow

__all__ = ["MainWindow"]
