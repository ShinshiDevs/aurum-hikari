from collections.abc import Sequence

__all__: Sequence[str] = ("AurumException",)


class AurumException(Exception):
    """Base exception of Aurum."""


class TaskException(AurumException):
    """Exception for tasks."""
