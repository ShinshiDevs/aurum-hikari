from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Type

import attrs
from hikari.events.base_events import EventT

if TYPE_CHECKING:
    from hikari.api.event_manager import CallbackT


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Event:
    event_types: Sequence[Type[EventT]]
    callback: CallbackT[EventT]
