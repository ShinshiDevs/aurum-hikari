from __future__ import annotations

import typing

from aurum.l10n.localization_provider_interface import LocalizationProviderInterface

if typing.TYPE_CHECKING:
    from aurum.l10n.localized import Localized


class PassLocalizationProvider(LocalizationProviderInterface):
    async def start(self) -> None:
        pass

    def build_localized(self, value: Localized) -> typing.Dict[str, str]:
        return {}

    def get_locale(self, by: typing.Any) -> None:
        pass
