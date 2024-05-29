from __future__ import annotations

__author__: typing.Final[str] = "Shinshi Developers Team"
__copyright__: typing.Final[str] = "Copyright (c) 2024 Shinshi Developers Team"
__license__: typing.Final[str] = "MIT"

__all__: Sequence[str] = (
    "__author__",
    "__copyright__",
    "__license__",
    "__version_tuple__",
    "__version__",
)

import typing

from aurum.internal.version import Version

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

__version_tuple__: Version = Version(0, 1, 5, 5)
__version__: str = str(__version_tuple__)
