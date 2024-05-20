from __future__ import annotations

import typing

from hikari.permissions import Permissions
from hikari.undefined import UNDEFINED

from aurum.internal.commands.app_command import AppCommand
from aurum.internal.exceptions.base_exception import AurumException

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

    from hikari.guilds import PartialGuild
    from hikari.snowflakes import SnowflakeishOr
    from hikari.undefined import UndefinedType

    from aurum.client import Client
    from aurum.includable import Includable
    from aurum.l10n import LocalizedOr
    from aurum.types import BotT


class Plugin:
    """
    Plugins include commands and components and provide bot, client, and etc.

    Attributes:
        name (str): The plugin name.
        description (LocalizedOr[str] | None): Optional description of the plugin.
        guild (SnowflakeishOr[PartialGuild] | UndefinedType): Optional guild (server) where the plugin is available.
        default_member_permissions (Permissions): The permissions a user must have to use the plugin by default.
        dm_enabled (bool): Whether the plugin can be used in direct messages.
        is_nsfw (bool): Indicates whether the plugin is age-restricted.
        included (Dict[str, Includable]): Included objects of plugin.

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
        "_bot",
        "_client",
        "name",
        "description",
        "guild",
        "default_member_permissions",
        "is_dm_enabled",
        "is_nsfw",
        "included",
    )

    def __init__(
        self,
        name: str,
        description: LocalizedOr[str] | None = None,
        *,
        guild: SnowflakeishOr[PartialGuild] | UndefinedType = UNDEFINED,
        default_member_permissions: Permissions = Permissions.NONE,
        is_dm_enabled: bool = False,
        is_nsfw: bool = False,
    ) -> None:
        self._bot: BotT | None = None
        self._client: Client | None = None

        self.name: str = name
        self.description: LocalizedOr[str] | None = description

        self.guild: SnowflakeishOr[PartialGuild] | UndefinedType = guild
        self.default_member_permissions: Permissions = default_member_permissions
        self.is_dm_enabled: bool = is_dm_enabled
        self.is_nsfw: bool = is_nsfw

        self.included: typing.Dict[str, Includable] = {}

    @property
    def bot(self) -> BotT | None:
        return self._bot

    @bot.setter
    def bot(self, bot: BotT) -> None:
        self._bot = bot

    @property
    def client(self) -> Client | None:
        return self._client

    @client.setter
    def client(self, client: Client) -> None:
        self._client = client

    def include(self, includable: typing.Type[Includable]) -> None:
        if issubclass(includable, AppCommand):
            try:
                instance: AppCommand = (
                    includable()  # type: ignore
                    .set_guild(self.guild)
                    .set_default_member_permissions(self.default_member_permissions)
                    .set_is_dm_enabled(self.is_dm_enabled)
                    .set_is_nsfw(self.is_nsfw)
                )
            except ValueError:
                raise AurumException("`__init__` of base includable wasn't overrided")
            self.included[instance.name] = instance
