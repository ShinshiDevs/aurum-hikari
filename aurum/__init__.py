"""
Aurum - A flexible command & component handler.
"""

from collections.abc import Sequence

from aurum.client import *
from aurum.commands import *
from aurum.interactions import *
from aurum.l10n import *

__all__: Sequence[str] = (
    "__version__",
    "Client",
    "MessageCommand",
    "SlashCommand",
    "UserCommand",
    "InteractionContext",
    "LocalizationProviderInterface",
    "Locale",
    "Localized",
    "LocalizedOr",
)
__version__: str = "0.1.2-alpha"
