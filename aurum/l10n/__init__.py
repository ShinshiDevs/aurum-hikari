from __future__ import annotations

import typing

from .localization_provider_interface import LocalizationProviderInterface
from .types import Locale, Localized, LocalizedOr

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

__all__: Sequence[str] = (
    "LocalizationProviderInterface",
    "Locale",
    "Localized",
    "LocalizedOr",
)
