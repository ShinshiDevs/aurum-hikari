from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Dict, List, Tuple, Type

from hikari.events.base_events import EventT
from hikari.guilds import PartialGuild
from hikari.permissions import Permissions
from hikari.snowflakes import SnowflakeishOr
from hikari.traits import GatewayBotAware
from hikari.undefined import UNDEFINED, UndefinedType

from aurum.commands.app_command import AppCommand
from aurum.includable import Includable

if TYPE_CHECKING:
    from hikari.api.event_manager import CallbackT

    from aurum.client import Client


class Plugin:
    """
    Plugins include commands and components and provide bot, client, and etc.

    Arguments:
        name (str): The plugin name.
        guild (SnowflakeishOr[PartialGuild] | UndefinedType): Optional guild (server) where the plugin is available.
        default_member_permissions (Permissions): The permissions a user must have to use the plugin by default.
        is_dm_enabled (bool): Whether the plugin can be used in direct messages.
        is_nsfw (bool): Indicates whether the plugin is age-restricted.
        override (bool): Boolean flag to override commands attributes.
            If override is set to True, the values for guild, default_member_permissions, is_dm_enabled,
            and is_nsfw will be overridden.

    Attributes:
        included (Dict[str, Includable]): Included objects of plugin.
        events (List[Event]): Events of plugin.

    Example:
        ```py
        plugin = Plugin(
            "Admin Plugin",
            default_member_permissions=Permissions.ADMINISTRATOR
        )


        @plugin.include
        class BanHammerCommand(SlashCommand):
            def __init__(self) -> None:
                super().__init__(
                    name="ban",
                    options=[
                        Option(
                            type=OptionType.USER,
                            name="target",
                            description="Who was bad today?"
                        )
                    ]
                )

            async def callback(self, context: InteractionContext, target: InteractionMember | User) -> None:
                await context.guild.ban(target)
                return await context.create_response("**@{target.username}** was ban hammered!")
        ```
    """

    __slots__: Sequence[str] = (
        "bot",
        "client",
        "name",
        "guild",
        "default_member_permissions",
        "is_dm_enabled",
        "is_nsfw",
        "override",
        "included",
        "events",
    )

    def __init__(
        self,
        name: str,
        *,
        guild: SnowflakeishOr[PartialGuild] | UndefinedType = UNDEFINED,
        default_member_permissions: Permissions = Permissions.NONE,
        is_dm_enabled: bool = False,
        is_nsfw: bool = False,
        override: bool = True,
    ) -> None:
        self.bot: GatewayBotAware
        self.client: Client

        self.name: str = name

        self.guild: SnowflakeishOr[PartialGuild] | UndefinedType = guild
        self.default_member_permissions: Permissions = default_member_permissions
        self.is_dm_enabled: bool = is_dm_enabled
        self.is_nsfw: bool = is_nsfw
        self.override: bool = override

        self.included: Dict[str, Includable] = {}
        self.events: List[Tuple[Sequence[EventT], CallbackT]] = []  # type: ignore

    def __call__(self, bot: GatewayBotAware, client: Client) -> Plugin:
        self.bot = bot
        self.client = client
        for event in self.events:  # type: ignore
            bot.event_manager.listen(*event[0])(event[1])  # type: ignore
        return self

    def include(self, includable: Type[Includable]) -> None:
        if issubclass(includable, AppCommand):
            command: AppCommand = includable()  # type: ignore
            if self.override:
                command.guild = self.guild
                command.default_member_perimssions = self.default_member_permissions
                command.is_dm_enabled = self.is_dm_enabled
                command.is_nsfw = self.is_nsfw
            self.included[command.name] = command

    def listen(self, *event_types: Type[EventT]) -> Callable[[CallbackT[EventT]], None]:
        def decorator(callback: CallbackT[EventT]) -> None:
            self.events.append((event_types, callback))  # type: ignore

        return decorator
