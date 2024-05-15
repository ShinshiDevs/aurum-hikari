from __future__ import annotations

import typing

from hikari.commands import CommandType
from hikari.permissions import Permissions

from aurum.commands.app_command import AppCommand

if typing.TYPE_CHECKING:
    from hikari.guilds import PartialGuild
    from hikari.messages import Message
    from hikari.snowflakes import SnowflakeishOr

    from aurum.l10n.types import LocalizedOr


class MessageCommand(AppCommand):
    """
    Represents a message-command.

    Attributes:
        Inherited from AppCommand class.

    Args:
        name (str): The unique name of the command.
        display_name (LocalizedOr[str] | None): The localized name of the command.
        guild (SnowflakeishOr[PartialGuild] | None): The guild in which the command is available.
        default_member_permissions (Permissions): Permissions required to use the command, if any. Defaults to NONE.
        dm_enabled (bool): Flag indicating whether the command is available in direct messages. Defaults to `False`.
        is_nsfw (bool): Flag indicating whether the command should only be available in NSFW channels. Defaults to `False`.

    Methods:
        Inherited from AppCommand class.

    Raises:
        NotImplementedError: This method should be overridden in a subclass and will raise an exception if called directly.
    """

    def __init__(
        self,
        name: str,
        *,
        display_name: LocalizedOr[str] | None = None,
        guild: SnowflakeishOr[PartialGuild] | None = None,
        default_member_permissions: Permissions = Permissions.NONE,
        dm_enabled: bool = False,
        is_nsfw: bool = False,
    ) -> None:
        super().__init__(
            command_type=CommandType.MESSAGE,
            name=name,
            description=None,
            display_name=display_name,
            guild=guild,
            default_member_permissions=default_member_permissions,
            dm_enabled=dm_enabled,
            is_nsfw=is_nsfw,
        )

    async def callback(self, context: InteractionContext, message: Message) -> None:
        raise NotImplementedError()
