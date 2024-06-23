from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Type

from hikari.events.base_events import EventT

if TYPE_CHECKING:
    from hikari.api.event_manager import CallbackT


@dataclass(kw_only=True, slots=True)
class Event:
    event_types: Sequence[Type[EventT]]
    callback: CallbackT[EventT]
