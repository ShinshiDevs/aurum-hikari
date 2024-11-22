from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import TYPE_CHECKING

from hikari.locales import Locale

if TYPE_CHECKING:
    from typing import Any

    from hikari.snowflakes import Snowflakeish

    from aurum.commands.base_command import BaseCommand

    CommandMapping = dict[Snowflakeish, BaseCommand]
    CommandCallbackT = Callable[..., Coroutine[Any, Any, None]]

Localized = dict[Locale | str, str]
