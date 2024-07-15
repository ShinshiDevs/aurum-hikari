from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from typing import TYPE_CHECKING, TypeVar

import attrs
from hikari.impl import AutocompleteChoiceBuilder
from hikari.interactions import AutocompleteInteractionOption

if TYPE_CHECKING:
    from aurum.context import AutocompleteContext

__all__: Sequence[str] = ("AutocompleteChoice",)


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class AutocompleteChoice:
    """Represents the autocomplete choice."""

    name: str = attrs.field(eq=False)
    value: int | str | float = attrs.field(eq=False)

    def to_builder(self) -> AutocompleteChoiceBuilder:
        return AutocompleteChoiceBuilder(name=self.name, value=self.value)


AutocompleteCallbackT = TypeVar(
    "AutocompleteCallbackT",
    bound=Callable[
        ["AutocompleteContext", AutocompleteInteractionOption],
        Awaitable[Sequence[AutocompleteChoice]],
    ],
)
