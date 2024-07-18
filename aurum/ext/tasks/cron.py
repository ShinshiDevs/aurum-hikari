from __future__ import annotations

import warnings
from asyncio.events import AbstractEventLoop, TimerHandle, get_event_loop
from collections.abc import Callable, Sequence
from datetime import datetime, timedelta, timezone
from logging import Logger, getLogger
from typing import TYPE_CHECKING

from aurum.exceptions import TaskException
from aurum.ext.tasks.base_task import BaseTask
from aurum.ext.tasks.typing import TaskCallbackT

if TYPE_CHECKING:
    from aurum.client import Client

try:
    import croniter
except ImportError:
    raise TaskException("Cannot work with cron tasks, because croniter is not installed")

__slots__: Sequence[str] = ("CronTask", "cron_task")


class CronTask(BaseTask):
    """Task class.

    Arguments:
        callback (TaskCallbackT[CronTask]): Callback of the task.
        crontab (str): Instruction for the croniter.
        name (str | None): Name of the task.

    Attributes:
        event_loop (AbstractEventLoop): Event loop to which the task is attached.
        handler (TimerHandle): Handler of the task.
        client (Client | None): The client that the task is linked to.
        name (str): Name of the task.
        callback (Callable[..., Any]): Callback of the task.
        croniter (croniter): Execution instruction.
    """

    __slots__: Sequence[str] = (
        "__logger",
        "handler",
        "event_loop",
        "client",
        "name",
        "callback",
        "croniter",
    )

    def __init__(
        self,
        callback: TaskCallbackT[CronTask],
        crontab: str,
        *,
        name: str | None = None,
    ) -> None:
        self.__logger: Logger = getLogger(f"aurum.tasks.{name or callback.__name__}")

        self.event_loop: AbstractEventLoop | None = None
        self.handler: TimerHandle | None = None
        self.client: Client | None = None

        self.name: str | None = name
        self.callback: TaskCallbackT[CronTask] = callback

        self.croniter = croniter.croniter(crontab, datetime.now(timezone.utc))

    @property
    def running(self) -> bool:
        return isinstance(self.handler, TimerHandle)

    def get_delay(self) -> timedelta:
        return self.croniter.get_next(datetime) - datetime.now(timezone.utc)

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
        self.__logger.debug("started, next execution will be in %s", self.get_delay())

    def stop(self) -> None:
        if self.handler:
            self.handler.cancel()
            self.__logger.debug("stopped")

    def run(self) -> None:
        assert isinstance(self.event_loop, AbstractEventLoop)
        self.event_loop.create_task(self.callback(self))  # type: ignore
        self.handler = self.event_loop.call_later(self.get_delay().total_seconds(), self.run)

    def set_crontab(self, crontab: str):
        self.croniter = croniter.croniter(crontab, datetime.now(timezone.utc))
        if self.handler:
            self.handler.cancel()
            self.run()
            self.__logger.debug("updated delay, next execution will be in %s", self.get_delay())


def cron_task(
    crontab: str,
    *,
    name: str | None = None,
) -> Callable[[TaskCallbackT[CronTask]], CronTask]:
    """Decorator for task definition."""

    def decorator(callback: TaskCallbackT[CronTask]) -> CronTask:
        return CronTask(
            callback=callback,
            crontab=crontab,
            name=name,
        )

    return decorator
