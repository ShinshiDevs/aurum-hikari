from __future__ import annotations

import abc
from collections.abc import Sequence
from types import TracebackType
from typing import TYPE_CHECKING, Tuple, Type

import attrs
from hikari.events import Event
from hikari.traits import RESTAware

from aurum.commands.app_command import AppCommand
from aurum.context import InteractionContext

if TYPE_CHECKING:
    from aurum.client import Client


__all__: Sequence[str] = ("AurumEvent", "ExceptionEvent", "CommandErrorEvent")


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class AurumEvent(Event, abc.ABC):
    """
    The base class for all Aurum's events.
    """

    app: RESTAware = attrs.field()
    """Instance of main application"""

    client: Client = attrs.field()
    """Client"""


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class ExceptionEvent(AurumEvent, abc.ABC):
    """
    Base class of events, that associated with exceptions.
    """

    exc_info: Tuple[Type[BaseException], BaseException, TracebackType | None]
    """Exception triplet."""

    exception: Exception
    """Exception that was raised."""


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class InteractionErrorEvent(ExceptionEvent, abc.ABC):
    """
    Event that being dispatched, when command execution has exceptions.
    """

    context: InteractionContext
    """Context of interaction."""


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class CommandErrorEvent(InteractionErrorEvent, abc.ABC):
    """
    Event that being dispatched, when command execution has exceptions.
    """

    command: AppCommand
    """Command with that occurred exception."""
