from __future__ import annotations

__author__: typing.Final[str] = "Shinshi Developers Team"
__copyright__: typing.Final[str] = "Copyright (c) 2024 Shinshi Developers Team"
__license__: typing.Final[str] = "MIT"

__all__: Sequence[str] = (
    "__author__",
    "__copyright__",
    "__license__",
    "__version__",
)

import typing

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

with open("VERSION") as stream:
    __version__: str = stream.readline()
