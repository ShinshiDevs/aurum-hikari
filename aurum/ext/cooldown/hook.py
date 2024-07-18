from collections.abc import Awaitable, Callable
from datetime import timedelta

from aurum.context import InteractionContext
from aurum.ext.cooldown.bucket import BucketType
from aurum.ext.cooldown.cooldown import Cooldown
from aurum.ext.cooldown.exceptions import CooldownException
from aurum.hooks import Hook, HookResult, hook


async def default_response(context: InteractionContext, error: CooldownException) -> None:
    await context.create_response(
        f"You're on cooldown, please retry after {round(error.retry_after)} seconds."
    )


def cooldown(
    delay: timedelta,
    *,
    capacity: int = 1,
    bucket: BucketType = BucketType.USER,
    response: Callable[[InteractionContext, CooldownException], Awaitable[None]] = default_response,
) -> Hook:
    """
    Returns a hook for applying a cooldown to a command.

    Arguments:
        delay (timedelta): The time delay for the cooldown.
        capacity (int, optional): The allowed capacity within the cooldown period. Defaults to 1.
        bucket (BucketType, optional): The type of bucket for specifying the cooldown scope.
        response (Callable[[InteractionContext, CooldownException], Awaitable[None]], optional):
            The response function to handle the cooldown exception.

    Returns:
        Hook: The cooldown hook.
    """
    cls: Cooldown = Cooldown(
        delay=delay,
        capacity=capacity,
        bucket=bucket,
    )

    @hook()
    async def cooldown_hook(context: InteractionContext) -> HookResult:
        try:
            cls.proceed(context)
        except CooldownException as error:
            await response(context, error)
            return HookResult(stop=True)
        return HookResult()

    return cooldown_hook
