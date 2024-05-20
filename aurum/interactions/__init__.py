from __future__ import annotations

__all__: Sequence[str] = ("InteractionContext",)

import typing

from .interaction_context import InteractionContext

if typing.TYPE_CHECKING:
    from collections.abc import Sequence
