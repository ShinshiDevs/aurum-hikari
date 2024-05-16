from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from hikari import CommandInteraction, ComponentInteraction

    from aurum.l10n.types import Locale, Localized


class LocalizationProviderInterface(typing.Protocol):
    async def start(self) -> None: ...

    def build_localized(self, value: Localized) -> typing.Dict[str, str]: ...

    def get_locale_from_interaction(
        self, interaction: CommandInteraction | ComponentInteraction
    ) -> Locale: ...
