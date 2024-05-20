from __future__ import annotations

__all__: Sequence[str] = ("Client",)

import typing

from .client import Client

if typing.TYPE_CHECKING:
    from collections.abc import Sequence
