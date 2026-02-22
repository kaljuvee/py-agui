"""
py-agui: Python Agentic UI - Real-time agentic chat interfaces with FastHTML
"""
from .core import setup_agui, AGUISetup, AGUIThread
from .styles import get_chat_styles, get_custom_theme
from .layouts import (
    chat_with_sidebar,
    simple_chat,
    three_pane_layout,
)

try:
    from importlib.metadata import version, PackageNotFoundError
    __version__ = version("py-agui")
except PackageNotFoundError:
    __version__ = "0.1.0-dev"

__all__ = [
    "setup_agui",
    "AGUISetup",
    "AGUIThread",
    "get_chat_styles",
    "get_custom_theme",
    "chat_with_sidebar",
    "simple_chat",
    "three_pane_layout",
    "__version__",
]
