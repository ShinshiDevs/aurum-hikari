from __future__ import annotations

import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from aurum.l10n.types import LocalizedOr


@dataclass(slots=True, kw_only=True)
class Choice:
    """Represents the option's choice"""

    name: LocalizedOr[str]
    value: typing.Any
