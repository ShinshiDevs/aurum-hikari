"""Aurum - A flexible framework for handling commands and components."""

from __future__ import annotations

__author__: Final[str] = "Shinshi Developers Team"
__copyright__: Final[str] = "Copyright (c) 2024 Shinshi Developers Team"
__license__: Final[str] = "MIT"
__all__: Sequence[str] = (
    "Client",
    "MessageCommand",
    "SlashCommand",
    "UserCommand",
    "sub_command",
    "InteractionContext",
    "LocalizationProviderInterface",
    "Localized",
    "LocalizedOr",
    "Option",
    "Choice",
    "AutocompleteChoice",
    "AutocompleteContext",
    "AurumEvent",
    "ExceptionEvent",
    "InteractionEvent",
    "CommandErrorEvent",
    "AurumException",
    "TaskException",
    "CooldownException",
    "HookResult",
    "Hook",
    "hook",
    "SyncCommandsFlag",
)

from collections.abc import Sequence
from typing import Final

from aurum.autocomplete import *
from aurum.client import *
from aurum.commands import *
from aurum.commands.decorators import *
from aurum.commands.enum import *
from aurum.context import *
from aurum.events import *
from aurum.exceptions import *
from aurum.hooks import *
from aurum.l10n import *
from aurum.option import *
from aurum.version import Version

__version__: Version = Version(0, 1, 6, 0)
