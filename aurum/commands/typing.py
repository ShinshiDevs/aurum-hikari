from collections.abc import Awaitable
from typing import Any, Callable

CommandCallbackT = Callable[..., Awaitable[Any]]
