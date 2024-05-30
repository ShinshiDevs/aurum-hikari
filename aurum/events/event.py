from __future__ import annotations

import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

    from hikari.api.event_manager import CallbackT
    from hikari.events.base_events import EventT


@dataclass(kw_only=True, slots=True)
class Event:
    event_types: Sequence[typing.Type[EventT]]
    callback: CallbackT[EventT]
