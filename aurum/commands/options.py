from collections.abc import Sequence
from typing import Any

import attrs
from hikari.channels import ChannelType
from hikari.commands import OptionType

from aurum.commands.types import Localized

__all__: Sequence[str] = ("Choice", "Option")


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Choice:
    """A choice option for slash commands.

    Parameters
    ----------
    name : str
        The name of the choice
    value : Any
        The value that will be passed to the command when this choice is selected
    name_localizations : Localized or None, optional
        The localizations of the choice name
    """

    name: str = attrs.field(eq=False)
    value: Any = attrs.field(eq=False)

    name_localizations: Localized | None = attrs.field(default=None, eq=False, repr=False)


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Option:
    """An option for a slash command.

    Parameters
    ----------
    type : OptionType
        The type of the option.
    name : str
        Name of the option.
    name_localizations : Localized or None, optional
        The option name localizations.
    description : str or None, optional
        Description of the option
    description_localizations : Localized or None, optional
        Localized descriptions for different languages
    choices : Sequence[Choice], optional
        Available choices for this option
    is_required : bool, optional
        Whether this option is required
    max_length : int or None, optional
        Maximum length for string input (string options only)
    min_length : int or None, optional
        Minimum length for string input (string options only)
    max_value : int or None, optional
        Maximum value for number input (integer options only)
    min_value : int or None, optional
        Minimum value for number input (integer options only)
    channel_types : Sequence[ChannelType], optional
        Allowed channel types (channel options only)
    """

    type: OptionType = attrs.field(eq=True)

    name: str = attrs.field(eq=True)
    name_localizations: Localized | None = attrs.field(default=None, eq=False, repr=False)
    description: str | None = attrs.field(default=None, repr=False, eq=False)
    description_localizations: Localized | None = attrs.field(default=None, eq=False, repr=False)

    choices: Sequence[Choice] = attrs.field(factory=tuple, repr=False, eq=False)

    is_required: bool = attrs.field(default=True, repr=True, eq=False)
    max_length: int | None = attrs.field(default=None, repr=False, eq=False)
    min_length: int | None = attrs.field(default=None, repr=False, eq=False)
    max_value: int | None = attrs.field(default=None, repr=False, eq=False)
    min_value: int | None = attrs.field(default=None, repr=False, eq=False)
    channel_types: Sequence[ChannelType] = attrs.field(factory=tuple, repr=False, eq=False)
