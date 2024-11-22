from logging import Logger, getLogger
from typing import Any

from hikari.internal.ux import TRACE

_TRACE_LOGGER: Logger = getLogger("aurum.trace")
_TRACE_LOGGER.setLevel(TRACE)


def trace(message: str, *args: Any, **kwargs: Any) -> None:
    _TRACE_LOGGER.debug(message, *args, **kwargs)
