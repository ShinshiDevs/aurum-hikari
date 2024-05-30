from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from hikari import GatewayBot

BotT = typing.TypeVar("BotT", bound=GatewayBot)
"""Type of bot"""
