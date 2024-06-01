from __future__ import annotations

__all__: Sequence[str] = ("Event",)

import typing

from .event import Event

if typing.TYPE_CHECKING:
    from collections.abc import Sequence
