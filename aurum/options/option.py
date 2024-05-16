from __future__ import annotations

import typing
from dataclasses import dataclass, field

from hikari.channels import ChannelType

from aurum.options.choice import Choice

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

    from hikari.commands import OptionType

    from aurum.l10n.types import LocalizedOr


@dataclass(slots=True, kw_only=True)
class Option:
    type: OptionType

    name: LocalizedOr[str]
    description: LocalizedOr[str]

    is_required: bool = True
    choices: Sequence[Choice] = field(default_factory=tuple[Choice])

    max_length: int | None = None
    min_length: int | None = None
    """Only for string option"""
    max_value: int | None = None
    min_value: int | None = None
    """Only for integer/float option"""
    channel_types: Sequence[ChannelType] = field(default_factory=tuple[ChannelType])
    """Only for channel option"""
