from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import TYPE_CHECKING, Any

from hikari.locales import Locale
from hikari.snowflakes import Snowflakeish

if TYPE_CHECKING:
    from aurum.commands.base_command import BaseCommand


Localized = dict[Locale | str, str]
CommandMapping = dict[Snowflakeish, "BaseCommand"]
CommandCallbackT = Callable[..., Coroutine[Any, Any, None]]
