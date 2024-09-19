from __future__ import annotations

from collections.abc import Sequence

__all__: Sequence[str] = ("AurumException", "TaskException")


class AurumException(Exception):
    """Base exception of Aurum."""


class TaskException(AurumException):
    """Exception for tasks."""
