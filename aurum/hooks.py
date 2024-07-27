from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from typing import TypeVar

import attrs

from aurum.context import InteractionContext

__all__: Sequence[str] = ("HookResult", "Hook", "hook")


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class HookResult:
    """The result of a hook callback."""

    stop: bool = attrs.field(default=False, eq=False)
    """Will hook stop execution or not."""


HookCallbackT = TypeVar(
    "HookCallbackT", bound=Callable[[InteractionContext], Awaitable[HookResult]]
)


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Hook:
    """Represents a hook."""

    callback: HookCallbackT
    """Callback of hook."""


def hook() -> Callable[[HookCallbackT], Hook]:
    """Decorator for defining a hook.

    Example:
        ```py
        @hook
        async def stop_hook(context: InteractionContext) -> HookResult:
            await context.create_response("No one will execute this command.")
            return HookResult(stop=True)
        ```
    """

    def decorator(callback: HookCallbackT) -> Hook:
        return Hook(callback=callback)

    return decorator
