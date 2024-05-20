from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from hikari import CommandInteraction, ComponentInteraction

    from aurum.l10n.locale import Locale
    from aurum.l10n.types import LocalizedOr


class LocalizationProviderInterface(typing.Protocol):
    """Localization provider interface.

    It's used to localize commands, components, and provide a locale for interaction.

    To get started with localization, you can either use our existing implementation (which is not available yet :d)
    or create your own.
    To create your own implementation, you need to inherit from this interface.
    """

    async def start(self) -> None:
        """Start the localization provider.

        Warning:
            Important function, must be implemented.
        """
        ...

    def build_localized(self, value: LocalizedOr[str]) -> typing.Dict[str, str]:
        """Build [Localized object][aurum.l10n.localized.Localized] for Discord API.

        Warning:
            - Important function, must be implemented.
            - When str is passed to value, this function must return empty dictionary.
        """
        ...

    def get_locale(self, by: str | CommandInteraction | ComponentInteraction) -> Locale | None:
        """Get locale by name or interaction"""
        ...
