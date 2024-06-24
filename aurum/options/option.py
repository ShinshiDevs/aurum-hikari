from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from hikari.channels import ChannelType
from hikari.commands import OptionType

from aurum.l10n.localized import Localized
from aurum.l10n.types import LocalizedOr
from aurum.options.choice import Choice


@dataclass(slots=True, kw_only=True)
class Option:
    """Represents the command option."""

    type: OptionType
    """The option type"""
    name: str
    """The unique name of the option"""
    display_name: LocalizedOr[str] | None = None
    """Display name of option.
    
    Can be localized."""
    description: LocalizedOr[str] = "No description"
    """The description of the option"""
    is_required: bool = True
    """An optional flag is the option is required.
    
    Default: True"""
    choices: Sequence[Choice] = field(default_factory=tuple)
    """A list of choices to the option"""
    max_length: int | None = None
    """An optional maximum length of the option value.

    Note:
        Available only for the string option type.
    """
    min_length: int | None = None
    """An optional minimum length of the option value.

    Note:
        Available only for the string option type.
    """
    max_value: int | None = None
    """An optional maximum value of the option value.

    Note:
        Available only for the integer/float option type.
    """
    min_value: int | None = None
    """An optional minimum value of the option value.

    Note:
        Available only for the integer/float option type.
    """
    channel_types: Sequence[ChannelType] = field(default_factory=tuple)
    """An optional channel types are available for selection.

    Note:
        Available only for the channel option type.
    """
