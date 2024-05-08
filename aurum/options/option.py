from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Tuple

from hikari.channels import ChannelType
from hikari.commands import OptionType

from aurum.i18n.translatable import Translatable
from aurum.options.choice import Choice


@dataclass(kw_only=True, slots=True)
class Option:
    type: OptionType

    name: Translatable | str
    description: Translatable | str | None = None

    choices: Tuple[Choice, ...] = field(default_factory=tuple)

    is_required: bool = True

    min_length: int | None = None
    max_length: int | None = None

    min_value: int | None = None
    max_value: int | None = None

    channel_types: Sequence[ChannelType] | None = None
