from __future__ import annotations

import typing

from .choice import Choice
from .option import Option

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

__all__: Sequence[str] = ("Choice", "Option")
