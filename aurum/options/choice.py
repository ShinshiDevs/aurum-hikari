from typing import Any
from dataclasses import dataclass

from aurum.l10n.types import LocalizedOr


@dataclass(slots=True, kw_only=True)
class Choice:
    """Represents the option's choice"""

    name: LocalizedOr[str]
    value: Any
