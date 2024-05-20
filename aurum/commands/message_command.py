from __future__ import annotations

import typing

from hikari.commands import CommandType
from hikari.permissions import Permissions
from hikari.undefined import UNDEFINED

from aurum.internal.commands.context_menu_command import ContextMenuCommand

if typing.TYPE_CHECKING:
    from hikari.guilds import PartialGuild
    from hikari.messages import Message
    from hikari.snowflakes import SnowflakeishOr
    from hikari.undefined import UndefinedType

    from aurum.interactions import InteractionContext


class MessageCommand(ContextMenuCommand):
    """Represents an application command for message's context menu.

    Args:
        name (str): The unique name of the command.
        guild (SnowflakeishOr[PartialGuild] | UndefinedType): Optional guild (server) where the command is available.
        default_member_permissions (Permissions): The permissions a user must have to use the command by default.
        is_dm_enabled (bool): Whether the command can be used in direct messages.
        is_nsfw (bool): Indicates whether the command is age-restricted.

    Example:
        ```py
        class ReverseTextCommand(MessageCommand):
            def __init__(self) -> None:
                super().__init__(name="Reverse", is_dm_enabled=True)

            async def callback(self, context: InteractionContext, message: Message) -> None:
                await context.create_response(message.content[::-1])
        ```
    """

    def __init__(
        self,
        name: str,
        *,
        guild: SnowflakeishOr[PartialGuild] | UndefinedType = UNDEFINED,
        default_member_permissions: Permissions = Permissions.NONE,
        is_dm_enabled: bool = False,
        is_nsfw: bool = False,
    ) -> None:
        super().__init__(
            command_type=CommandType.MESSAGE,
            name=name,
            guild=guild,
            default_member_permissions=default_member_permissions,
            is_dm_enabled=is_dm_enabled,
            is_nsfw=is_nsfw,
        )

    async def callback(self, context: InteractionContext, message: Message) -> None:
        """A callback of the command.

        Meant to override this method to set the callback to the command.

        Raises:
            NotImplementedError: If callback wasn't overrided.
        """
        raise NotImplementedError()
