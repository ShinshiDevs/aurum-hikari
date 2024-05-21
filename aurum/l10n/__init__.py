from __future__ import annotations

__all__: Sequence[str] = (
    "LocalizationProviderInterface",
    "Localized",
    "LocalizedOr",
)

import typing

from .localization_provider_interface import LocalizationProviderInterface
from .localized import Localized
from .types import LocalizedOr

if typing.TYPE_CHECKING:
    from collections.abc import Sequence
