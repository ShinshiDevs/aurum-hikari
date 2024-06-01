from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from collections.abc import Sequence


class Includable:
    """Class for includable objects"""

    __slots__: Sequence[str] = ("name",)

    def __init__(self, name: str) -> None:
        self.name: str = name
