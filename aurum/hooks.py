from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from typing import TypeVar

import attrs

from aurum.context import InteractionContext

__all__: Sequence[str] = ("HookResult", "Hook", "hook")


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class HookResult:
    """The result of a hook callback.

    Attributes:
        stop (bool): Will hook stop execution or not.
    """

    stop: bool = attrs.field(default=False, eq=False)


HookCallbackT = TypeVar(
    "HookCallbackT", bound=Callable[[InteractionContext], Awaitable[HookResult]]
)


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Hook:
    """Represents a hook.

    Attributes:
        callback (HookCallbackT): Callback of hook.
    """

    callback: HookCallbackT


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
        return Hook(
            callback=callback,
        )

    return decorator
