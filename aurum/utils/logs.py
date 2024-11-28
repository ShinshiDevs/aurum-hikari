from logging import Handler, Logger, getLogger
from typing import Any

from hikari.internal.ux import TRACE

_TRACE_HANDLER: Handler = Handler(level=TRACE)
_TRACE_LOGGER: Logger = getLogger("aurum.trace")
_TRACE_LOGGER.addHandler(_TRACE_HANDLER)


def trace(message: str, *args: Any, **kwargs: Any) -> None:
    _TRACE_LOGGER.debug(message, *args, **kwargs)
