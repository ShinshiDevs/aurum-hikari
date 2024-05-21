from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from hikari import CommandInteraction, ComponentInteraction

    from aurum.l10n.localized import Localized


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

    def build_localized(self, value: Localized) -> typing.Dict[str, str]:
        """Build [Localized object][aurum.l10n.localized.Localized] for Discord API.

        Warning:
            Important function, must be implemented.
        """
        ...

    def get_locale(self, by: str | CommandInteraction | ComponentInteraction) -> typing.Any:
        """Get locale by name or interaction"""
        ...
