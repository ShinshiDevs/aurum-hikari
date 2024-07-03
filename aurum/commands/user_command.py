from collections.abc import Sequence

from hikari.commands import CommandType
from hikari.interactions import InteractionMember
from hikari.users import PartialUser

from aurum.context import InteractionContext
from aurum.commands.context_menu_command import ContextMenuCommand


class UserCommand(ContextMenuCommand):
    """Represents an application command for user's context menu.

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
        class HelloUserCommand(UserCommand):
            def __init__(self) -> None:
                super().__init__(name="Hello to")

            async def callback(self, context: InteractionContext, target: InteractionMember | User) -> None:
                await context.create_response(f"Hi, {target.mention}!")
        ```
    """

    command_type: CommandType = CommandType.USER

    __slots__: Sequence[str] = (
        "app",
        "name",
        "display_name",
        "guild",
        "default_member_permissions",
        "dm_enabled",
        "is_nsfw",
    )

    async def callback(
        self, context: InteractionContext, target: InteractionMember | PartialUser
    ) -> None:
        """A callback of the command.

        Meant to override this method to set the callback to the command.

        Raises:
            NotImplementedError: If callback wasn't overrided.
        """
        raise NotImplementedError()
