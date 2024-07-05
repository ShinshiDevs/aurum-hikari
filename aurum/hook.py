from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import TypeVar

import attrs

from aurum.context import InteractionContext


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class HookResult:
    """The result of a hook callback."""

    stop: bool = attrs.field(default=False, eq=False)


HookCallbackT = TypeVar(
    "HookCallbackT", bound=Callable[[InteractionContext], Awaitable[HookResult]]
)


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Hook:
    """Represents a hook."""

    callback: HookCallbackT
    """The callback function."""


def hook() -> Callable[[HookCallbackT], Hook]:
    """Decorator for defining a hook."""

    def decorator(callback: HookCallbackT) -> Hook:
        return Hook(
            callback=callback,
        )

    return decorator
