from __future__ import annotations

__all__: Sequence[str] = ("AurumException", "UnknownCommandException")

import typing

from .base_exception import AurumException
from .commands_exceptions import UnknownCommandException

if typing.TYPE_CHECKING:
    from collections.abc import Sequence
