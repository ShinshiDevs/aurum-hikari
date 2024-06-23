from __future__ import annotations

__all__: Sequence[str] = (
    "LocalizationProviderInterface",
    "Localized",
    "LocalizedOr",
)

from collections.abc import Sequence

from .localization_provider_interface import LocalizationProviderInterface
from .localized import Localized
from .types import LocalizedOr
