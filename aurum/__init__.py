"""
Aurum - A flexible command & component handler.
"""

from collections.abc import Sequence
from importlib.metadata import version

from aurum.client import Client
from aurum.commands import *

__all__: Sequence[str] = (
    "__version__",
    "Client",
    "UserCommand",
    "MessageCommand",
)
__version__: str = version("aurum-hikari")
