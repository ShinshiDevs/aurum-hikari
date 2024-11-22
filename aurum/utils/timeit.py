import time
from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from typing import Any


@asynccontextmanager
async def timeit(_print: Callable[..., None] = print, *args: Any, **kwargs: Any) -> AsyncGenerator[Any, Any]:
    now: float = time.monotonic()
    try:
        yield
    finally:
        _print(*args, time.monotonic() - now, **kwargs)
