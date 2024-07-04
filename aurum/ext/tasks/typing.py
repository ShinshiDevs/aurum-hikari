from collections.abc import Callable, Coroutine
from typing import Any, TypeVar, Union

from aurum.ext.tasks.base_task import BaseTask

T = TypeVar("T", bound=BaseTask, contravariant=True)
TaskCallbackT = Union[Callable[[T], Coroutine[None, None, Any]], T]
