from __future__ import annotations

import typing

from hikari.commands import CommandType
from hikari.permissions import Permissions
from hikari.undefined import UNDEFINED

from aurum.internal.commands.context_menu_command import ContextMenuCommand

if typing.TYPE_CHECKING:
    from hikari.guilds import PartialGuild
    from hikari.interactions import InteractionMember
    from hikari.snowflakes import SnowflakeishOr
    from hikari.undefined import UndefinedType
    from hikari.users import PartialUser

    from aurum.interactions import InteractionContext


class UserCommand(ContextMenuCommand):
    """
    Represents a user-command.

    Raises:
        NotImplementedError: This method should be overridden in a subclass and will raise an exception if called directly.
    """

    def __init__(
        self,
        name: str,
        *,
        guild: SnowflakeishOr[PartialGuild] | UndefinedType = UNDEFINED,
        default_member_permissions: Permissions = Permissions.NONE,
        dm_enabled: bool = False,
        is_nsfw: bool = False,
    ) -> None:
        super().__init__(
            command_type=CommandType.USER,
            name=name,
            guild=guild,
            default_member_permissions=default_member_permissions,
            dm_enabled=dm_enabled,
            is_nsfw=is_nsfw,
        )

    async def callback(
        self, context: InteractionContext, target: InteractionMember | PartialUser
    ) -> None:
        raise NotImplementedError()
