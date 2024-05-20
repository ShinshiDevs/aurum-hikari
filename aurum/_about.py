from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

__all__: Sequence[str] = (
    "__version__",
    "__author__",
    "__copyright__",
    "__license__",
)
__version__: str = "0.1.4.1"
__author__: typing.Final[str] = "Shinshi Developers Team"
__copyright__: typing.Final[str] = "Copyright (c) 2024 Shinshi Developers Team"
__license__: typing.Final[str] = "MIT"
