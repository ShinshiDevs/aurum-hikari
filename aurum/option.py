from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import attrs
from hikari.channels import ChannelType
from hikari.commands import OptionType

from aurum.autocomplete import AutocompleteCallbackT
from aurum.l10n.types import LocalizedOr

__all__: Sequence[str] = ("Choice", "Option")


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Choice:
    """Represents the option's choice."""

    name: LocalizedOr[str] = attrs.field(eq=False)
    value: Any = attrs.field(eq=False)


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Option:
    """Represents the command option."""

    type: OptionType = attrs.field(eq=False)
    """The option type."""
    name: str = attrs.field(eq=False)
    """The unique name of the option."""
    display_name: LocalizedOr[str] | None = attrs.field(default=None, repr=False, eq=False)
    """Display name of option.

    Note:
        Can be localized.
    """
    description: LocalizedOr[str] = attrs.field(default="No description", repr=False, eq=False)
    """The description of the option."""
    is_required: bool = attrs.field(default=True, repr=True, eq=False)
    """An optional flag is the option is required.
    
    Default: True"""
    autocomplete: AutocompleteCallbackT | None = attrs.field(default=None, repr=True, eq=False)  # type: ignore
    """Autocomplete callback.
    
    When this argument is specified, the option becomes autocompletable.
    """
    choices: Sequence[Choice] = attrs.field(factory=tuple, repr=False, eq=False)
    """A list of choices to the option."""
    max_length: int | None = attrs.field(default=None, repr=False, eq=False)
    """An optional maximum length of the option value.

    Note:
        Available only for the string option type.
    """
    min_length: int | None = attrs.field(default=None, repr=False, eq=False)
    """An optional minimum length of the option value.

    Note:
        Available only for the string option type.
    """
    max_value: int | None = attrs.field(default=None, repr=False, eq=False)
    """An optional maximum value of the option value.

    Note:
        Available only for the integer/float option type.
    """
    min_value: int | None = attrs.field(default=None, repr=False, eq=False)
    """An optional minimum value of the option value.

    Note:
        Available only for the integer/float option type.
    """
    channel_types: Sequence[ChannelType] = attrs.field(factory=tuple, repr=False, eq=False)
    """An optional channel types are available for selection.

    Note:
        Available only for the channel option type.
    """
