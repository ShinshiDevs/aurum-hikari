from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from typing import Generic, TypeVar

import attrs

from aurum.context import InteractionContext

__all__: Sequence[str] = ("HookResult", "Hook", "hook")


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class HookResult:
    """The result of a hook callback."""

    stop: bool = attrs.field(default=False, eq=False)
    """Will hook stop execution or not."""


ContextT = TypeVar("ContextT", bound=InteractionContext)
HookCallbackT = Callable[[ContextT], Awaitable[HookResult]]


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Hook(Generic[ContextT]):
    """Represents a hook."""

    callback: HookCallbackT[ContextT]
    """Callback of hook."""


def hook() -> Callable[[HookCallbackT[ContextT]], Hook[ContextT]]:
    """Decorator for defining a hook.

    Example:
        ```py
        @hook()
        async def stop_hook(context: InteractionContext) -> HookResult:
            await context.create_response("No one will execute this command.")
            return HookResult(stop=True)
        ```
    """

    def decorator(callback: HookCallbackT[ContextT]) -> Hook[ContextT]:
        return Hook(callback=callback)

    return decorator
