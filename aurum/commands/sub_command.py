from collections.abc import Sequence
from dataclasses import dataclass, field

from aurum.i18n.translatable import Translatable


@dataclass(slots=True)
class SubCommand:
    name: str
    description: str | Translatable = "No description"

    options: Sequence[Option] = field(default_factory=tuple)
