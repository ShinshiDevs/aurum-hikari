from __future__ import annotations

import typing

from hikari.commands import CommandType
from hikari.permissions import Permissions

from aurum.commands.app_command import AppCommand

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

    from hikari.guilds import PartialGuild
    from hikari.snowflakes import SnowflakeishOr

    from aurum.commands.sub_commands import SubCommand
    from aurum.l10n.types import LocalizedOr
    from aurum.options import Option


class SlashCommand(AppCommand):
    """
    Represents a slash-command.

    Attributes:
        _app (PartialCommand): Command application instance, available after sync.
        command_type (CommandType): Type of the command.
        name (str): The internal name of the command used for identification, display if `display_name` is not provided.
        description (LocalizedOr[str] | None): Optional description of the command for help documentation.
        display_name (LocalizedOr[str] | None): Optional localized display name of the command.
        guild (SnowflakeishOr[PartialGuild] | None): Optional guild (server) where the command is available.
        default_member_permissions (Permissions): The permissions a user must have to use the command by default.
        dm_enabled (bool): Whether the command can be used in direct messages.
        is_nsfw (bool): Indicates whether the command is age-restricted.
        options (Sequence[Option]): Options to the command.
        sub_commands (Dict[str, SubCommand]): Sub-commands of the command.

    Args:
        name (str): The unique name of the command.
        description (LocalizedOr[str] | None): A description of command.
        display_name (LocalizedOr[str] | None): The localized name of the command.
        guild (SnowflakeishOr[PartialGuild] | None): The guild in which the command is available.
        default_member_permissions (Permissions): Permissions required to use the command, if any. Defaults to NONE.
        dm_enabled (bool): Flag indicating whether the command is available in direct messages. Defaults to `False`.
        is_nsfw (bool): Flag indicating whether the command should only be available in NSFW channels. Defaults to `False`.
        options (Sequence[Option]): Options to the command.

    Methods:
        Inherited from AppCommand class.

    Note:
        If your command has sub-commands, the callback will not be executed.
    """

    __slots__: Sequence[str] = (
        "_app",
        "command_type",
        "name",
        "description",
        "display_name",
        "guild",
        "default_member_permissions",
        "dm_enabled",
        "is_nsfw",
        "options",
        "sub_commands",
    )

    def __init__(
        self,
        name: str,
        description: LocalizedOr[str] | None = None,
        *,
        display_name: LocalizedOr[str] | None = None,
        guild: SnowflakeishOr[PartialGuild] | None = None,
        default_member_permissions: Permissions = Permissions.NONE,
        dm_enabled: bool = False,
        is_nsfw: bool = False,
        options: Sequence[Option] = (),
    ) -> None:
        super().__init__(
            command_type=CommandType.SLASH,
            name=name,
            description=description,
            display_name=display_name,
            guild=guild,
            default_member_permissions=default_member_permissions,
            dm_enabled=dm_enabled,
            is_nsfw=is_nsfw,
        )
        self.options: Sequence[Option] = options
        self.sub_commands: typing.Dict[str, SubCommand] = {}
