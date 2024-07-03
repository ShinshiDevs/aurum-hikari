from typing import Any, Dict, Protocol

from hikari.interactions import CommandInteraction, ComponentInteraction
from hikari.locales import Locale

from aurum.l10n.localized import Localized


class LocalizationProviderInterface(Protocol):
    """Localization provider interface.

    It's used to localize commands, components, and provide a locale for interaction.
    To create your own implementation, you need to inherit from this interface.
    """

    async def start(self) -> None:
        """Start the localization provider."""
        ...

    def build_localized(self, value: Localized) -> Dict[Locale | str, str]:
        """Build [Localized object][aurum.l10n.localized.Localized] for Discord API.

        !!! warning
            This function must change Localized object.

            The new value should include translations for the localized object and any new fallback.
            With the fallback, you can either use the first translation, translation with your default language,
            or take no action if there's a fallback.
        """
        ...

    def get_locale(self, by: str | CommandInteraction | ComponentInteraction) -> Any:
        """Get locale by name or interaction."""
        ...
