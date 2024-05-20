from __future__ import annotations

__all__: Sequence[str] = ("sub_command",)

import typing

from .sub_command import sub_command

if typing.TYPE_CHECKING:
    from collections.abc import Sequence
