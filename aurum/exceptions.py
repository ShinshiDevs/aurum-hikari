from collections.abc import Sequence
from typing import Any

from aurum.context import InteractionContext

__all__: Sequence[str] = ("AurumException",)


class AurumException(Exception):
    """Base exception of Aurum."""


class TaskException(AurumException):
    """Exception for tasks."""


class CooldownException(AurumException):
    def __init__(self, *args: Any, context: InteractionContext, retry_after: float) -> None:
        super().__init__(*args)
        self.context: InteractionContext = context
        self.retry_after: float = retry_after
