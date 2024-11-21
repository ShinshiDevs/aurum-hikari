from collections.abc import Sequence

from hikari.commands import CommandType
from hikari.messages import Message

from aurum.context import InteractionContext
from aurum.commands.context_menu_command import ContextMenuCommand


class MessageCommand(ContextMenuCommand):
    """Represents an application command for message's context menu.

    Args:
        name (str): The unique name of the command.
        display_name (LocalizedOr[str] | None): A display name of command.
            Can be localized.
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

    command_type: CommandType = CommandType.MESSAGE

    __slots__: Sequence[str] = ("name", "display_name", "dm_enabled")

    async def callback(self, context: InteractionContext, message: Message) -> None:
        """A callback of the command.

        Meant to override this method to set the callback to the command.

        Raises:
            NotImplementedError: If callback wasn't overrided.
        """
        raise NotImplementedError()
