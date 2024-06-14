from __future__ import annotations

__all__: Sequence[str] = ("Plugin", "PluginManager")

import typing

from .plugin import Plugin
from .plugin_manager import PluginManager

if typing.TYPE_CHECKING:
    from collections.abc import Sequence
