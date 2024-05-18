from __future__ import annotations

import typing

from .locale import Locale
from .localization_provider_interface import LocalizationProviderInterface
from .localized import Localized
from .types import LocalizedOr

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

__all__: Sequence[str] = (
    "LocalizationProviderInterface",
    "Locale",
    "Localized",
    "LocalizedOr",
)
