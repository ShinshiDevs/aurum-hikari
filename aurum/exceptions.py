from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from aurum.context import InteractionContext

if TYPE_CHECKING:
    from aurum.ext.cooldown.bucket import BucketType

__all__: Sequence[str] = ("AurumException", "TaskException", "CooldownException")


class AurumException(Exception):
    """Base exception of Aurum."""


class TaskException(AurumException):
    """Exception for tasks."""


class CooldownException(AurumException):
    """Exception raised when a user/guild encounters a rate limit error.

    Attributes:
        context (InteractionContext): The context of the interaction.
        retry_after (float): The time in seconds the client should wait before reissuing the request.
        bucket (BucketType): The type of rate limit bucket associated with the error.
    """

    def __init__(
        self, *args: Any, context: InteractionContext, retry_after: float, bucket: BucketType
    ) -> None:
        super().__init__(*args)
        self.context: InteractionContext = context
        self.retry_after: float = retry_after
        self.bucket: BucketType = bucket
