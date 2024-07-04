from __future__ import annotations

import warnings
from asyncio.events import AbstractEventLoop, TimerHandle, get_event_loop
from collections.abc import Callable
from datetime import timedelta
from logging import Logger, getLogger
from typing import TYPE_CHECKING, Sequence

from aurum.exceptions import TaskException
from aurum.ext.tasks.base_task import BaseTask
from aurum.ext.tasks.typing import TaskCallbackT

if TYPE_CHECKING:
    from aurum.client import Client

__slots__: Sequence[str] = ("Task", "task")


class Task(BaseTask):
    """Task class.

    Arguments:
        callback (Callable[..., Any]): Callback of the task.
        delay (timedelta): Cycle execution delay.
        name (str): Name of the task.

    Attributes:
        event_loop (AbstractEventLoop): Event loop to which the task is attached.
        handler (TimerHandle): Handler of the task.
        client (Client | None): The client that the task is linked to.
        name (str): Name of the task.
        callback (Callable[..., Any]): Callback of the task.
        delay (timedelta): Cycle execution delay.
    """

    __slots__: Sequence[str] = (
        "__logger",
        "handler",
        "event_loop",
        "client",
        "name",
        "callback",
        "delay",
    )

    def __init__(
        self,
        callback: TaskCallbackT[Task],
        delay: timedelta,
        *,
        name: str | None = None,
    ) -> None:
        self.__logger: Logger = getLogger(f"aurum.tasks.{name or callback.__name__}")

        self.event_loop: AbstractEventLoop | None = None
        self.handler: TimerHandle | None = None
        self.client: Client | None = None

        self.name: str | None = name
        self.callback: TaskCallbackT[Task] = callback

        self.delay: timedelta = delay

    @property
    def running(self) -> bool:
        return isinstance(self.handler, TimerHandle)

    def start(self, *, client: Client | None = None) -> None:
        if self.running:
            raise TaskException("Task is already running")
        if not self.event_loop:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                self.event_loop = get_event_loop()
        if not self.client:
            self.client = client
        self.run()
        self.__logger.debug("started, next execution will be in %s", self.delay)

    def stop(self) -> None:
        if self.handler:
            self.handler.cancel()
            self.__logger.debug("stopped")

    def run(self) -> None:
        assert isinstance(self.event_loop, AbstractEventLoop)
        self.event_loop.create_task(self.callback(self), name=self.name)  # type: ignore
        self.handler = self.event_loop.call_later(self.delay.total_seconds(), self.run)

    def set_delay(self, delay: timedelta):
        self.delay = delay
        if self.handler:
            self.handler.cancel()
            self.run()
            self.__logger.debug("updated delay, next execution will be in %s", self.delay)


def task(
    delay: timedelta,
    *,
    name: str | None = None,
) -> Callable[[TaskCallbackT[Task]], Task]:
    """Decorator for task definition."""

    def decorator(callback: TaskCallbackT[Task]) -> Task:
        return Task(
            callback=callback,
            delay=delay,
            name=name,
        )

    return decorator
