"""
Aurum - Flexible framework for command and component handling with integrations.
"""

from __future__ import annotations

__all__: Sequence[str] = (
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

import typing

from aurum.client import *
from aurum.commands import *
from aurum.interactions import *
from aurum.l10n import *
from aurum.options import *

if typing.TYPE_CHECKING:
    from collections.abc import Sequence
