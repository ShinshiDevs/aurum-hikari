from __future__ import annotations

__author__: Final[str] = "Shinshi Developers Team"
__copyright__: Final[str] = "Copyright (c) 2024 Shinshi Developers Team"
__license__: Final[str] = "MIT"

__all__: Sequence[str] = (
    "__author__",
    "__copyright__",
    "__license__",
    "__version_tuple__",
    "__version__",
)

from collections.abc import Sequence
from typing import Final

from aurum.internal.version import Version

__version_tuple__: Final[Version] = Version(0, 1, 5, 6)
__version__: Final[str] = str(__version_tuple__)
