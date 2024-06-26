from typing import Any

import attrs

from aurum.l10n.types import LocalizedOr


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Choice:
    """Represents the option's choice"""

    name: LocalizedOr[str]
    value: Any
