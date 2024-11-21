from typing import Any

from aurum.context import InteractionContext
from aurum.exceptions import AurumException
from aurum.ext.cooldown.bucket import BucketType


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