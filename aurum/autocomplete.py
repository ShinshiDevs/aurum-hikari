from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from typing import TYPE_CHECKING, Any, TypeVar

import attrs
from hikari import AutocompleteInteractionOption

if TYPE_CHECKING:
    from aurum.context import AutocompleteContext

__all__: Sequence[str] = ("AutocompleteChoice",)


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class AutocompleteChoice:
    """Represents the autocomplete choice."""

    name: str = attrs.field(eq=False)
    value: Any = attrs.field(eq=False)


AutocompleteCallbackT = TypeVar(
    "AutocompleteCallbackT",
    bound=Callable[
        ["AutocompleteContext", AutocompleteInteractionOption],
        Awaitable[Sequence[AutocompleteChoice]],
    ],
)
