import asyncio
from collections.abc import Sequence
from datetime import timedelta
from typing import Dict

import attrs
from hikari.snowflakes import Snowflake

from aurum.context import InteractionContext
from aurum.ext.cooldown.bucket import BucketType
from aurum.ext.cooldown.exceptions import CooldownException


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class CooldownEntity:
    """Represents an entity for managing cooldown information."""

    capacity: int = attrs.field(default=0, eq=False)
    handler: asyncio.TimerHandle | None = attrs.field(default=None, eq=False, repr=False)


class Cooldown:
    """Implements a cooldown mechanism for controlling command usage over time.

    Arguments:
        delay (float | timedelta): The time delay for the cooldown.
        capacity (int, optional): The allowed capacity within the cooldown period. Defaults to 1.
        bucket (BucketType, optional): The type of bucket for specifying the cooldown scope.
    """

    __slots__: Sequence[str] = ("event_loop", "delay", "capacity", "bucket", "limited")

    def __init__(
        self, delay: float | timedelta, *, capacity: int = 1, bucket: BucketType = BucketType.USER
    ) -> None:
        self.event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self.delay: float = delay.total_seconds() if isinstance(delay, timedelta) else delay
        self.capacity: int = capacity
        self.bucket: BucketType = bucket
        self.limited: Dict[Snowflake, CooldownEntity] = {}

    def unlimit(self, target: Snowflake, entity: CooldownEntity):
        """Unlimits the target entity from the cooldown."""
        del self.limited[target]
        del entity

    def proceed(self, context: InteractionContext) -> None:
        """
        Proceeds with the command invocation and applies the cooldown mechanism.

        Arguments:
            context (InteractionContext): The interaction context for the command invocation.

        Raises:
            CooldownException: If the cooldown limit is reached.
        """
        target: Snowflake = self.bucket[context.interaction]

        entity = self.limited.setdefault(target, CooldownEntity())
        entity.capacity += 1

        if entity.capacity > self.capacity:
            if not entity.handler:
                entity.handler = self.event_loop.call_later(
                    self.delay, self.unlimit, target, entity
                )
            raise CooldownException(
                context=context,
                retry_after=max(0, entity.handler.when() - self.event_loop.time()),
                bucket=self.bucket,
            )
