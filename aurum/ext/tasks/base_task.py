from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aurum.client import Client


class BaseTask(abc.ABC):
    """Base class for tasks."""

    @abc.abstractmethod
    def start(self, *, client: Client | None = None) -> None: 
        ...

    @abc.abstractmethod
    def stop(self) -> None: 
        ...

    @abc.abstractmethod
    def run(self) -> None: 
        ...
