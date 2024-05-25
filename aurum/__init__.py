"""Aurum - A flexible framework for handling commands and components with integrations."""

from __future__ import annotations

__all__: Sequence[str] = (
    "Client",
    "MessageCommand",
    "SlashCommand",
    "UserCommand",
    "InteractionContext",
    "LocalizationProviderInterface",
    "Localized",
    "LocalizedOr",
    "Option",
    "Choice",
)

import typing

from aurum.client import *
from aurum.commands import *
from aurum.interactions import *
from aurum.l10n import *
from aurum.options import *

if typing.TYPE_CHECKING:
    from collections.abc import Sequence
