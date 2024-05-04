import concurrent.futures
import os
from collections.abc import Sequence
from typing import Any, Dict, TYPE_CHECKING
from logging import getLogger

from hikari.events import StartedEvent
from hikari.snowflakes import Snowflakeish
from hikari.impl import config as config_impl
from hikari.intents import Intents
from hikari.impl import GatewayBot

from aurum.abc.hook import Hook
from aurum.commands.command_handler import CommandHandler

if TYPE_CHECKING:
    from logging import Logger


class Client(GatewayBot):
    """Base client

    Inherited from `hikari.impl.GatewayBot`
    """

    def __init__(
        self,
        token: str,
        *,
        model: Any = None,
        intents: Intents = Intents.ALL_UNPRIVILEGED,
        sync_commands: bool = True,
        auto_chunk_members: bool = True,
        default_guild: Snowflakeish | None = None,
        tracked_guilds: Sequence[Snowflakeish] | None = None,
        allow_unknown_interactions: bool = False,
        pre_command_hooks: Sequence[Hook] | None = None,
        post_command_hooks: Sequence[Hook] | None = None,
        banner: str | None = "hikari",
        allow_color: bool = True,
        force_color: bool = False,
        cache_settings: config_impl.CacheSettings | None = None,
        http_settings: config_impl.HTTPSettings | None = None,
        proxy_settings: config_impl.ProxySettings | None = None,
        logs: str | int | Dict[str, Any] | os.PathLike[str] | None = "INFO",
        max_rate_limit: float = 300.0,
        max_retries: int = 3,
        rest_url: str | None = None,
        executor: concurrent.futures.Executor | None = None,
    ) -> None:
        self.__logger: Logger = getLogger("aurum.client")
        self.model: Any = model
        super().__init__(
            token=token,
            intents=intents,
            auto_chunk_members=auto_chunk_members,
            banner=banner,
            allow_color=allow_color,
            force_color=force_color,
            cache_settings=cache_settings,
            http_settings=http_settings,
            proxy_settings=proxy_settings,
            logs=logs,
            max_rate_limit=max_rate_limit,
            max_retries=max_retries,
            rest_url=rest_url,
            executor=executor,
        )
        self.commands: CommandHandler = CommandHandler(
            allow_unknown_interactions,
            pre_command_hooks,
            post_command_hooks,
        )
        if sync_commands:
            self.event_manager.subscribe(StartedEvent, self.commands.sync)
