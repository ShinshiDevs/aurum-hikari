from __future__ import annotations

import typing

from hikari.permissions import Permissions

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

    from hikari.commands import CommandType, PartialCommand
    from hikari.guilds import PartialGuild
    from hikari.snowflakes import SnowflakeishOr

    from aurum.l10n.types import LocalizedOr


class AppCommand:
    """
    Represents a application command.

    !!! This class is not suitable for use, please use the pre-existing implementations.

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

    Args:
        name (str): The unique name of the command.
        description (LocalizedOr[str] | None): A description of command.
        display_name (LocalizedOr[str] | None): The localized name of the command.
        guild (SnowflakeishOr[PartialGuild] | None): The guild in which the command is available.
        default_member_permissions (Permissions): Permissions required to use the command, if any. Defaults to NONE.
        dm_enabled (bool): Flag indicating whether the command is available in direct messages. Defaults to `False`.
        is_nsfw (bool): Flag indicating whether the command should only be available in NSFW channels. Defaults to `False`.

    Methods:
        callback: An asynchronous method meant to be overridden that defines the command's callback.
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
    )

    def __init__(
        self,
        command_type: CommandType,
        name: str,
        description: LocalizedOr[str] | None = None,
        *,
        display_name: LocalizedOr[str] | None = None,
        guild: SnowflakeishOr[PartialGuild] | None = None,
        default_member_permissions: Permissions = Permissions.NONE,
        dm_enabled: bool = False,
        is_nsfw: bool = False,
    ) -> None:
        self._app: PartialCommand | None = None

        self.command_type: CommandType = command_type
        self.name: str = name
        self.description: LocalizedOr[str] | None = description

        self.display_name: LocalizedOr[str] | None = display_name
        self.guild: SnowflakeishOr[PartialGuild] | None = guild
        self.default_member_permissions: Permissions = default_member_permissions
        self.dm_enabled: bool = dm_enabled
        self.is_nsfw: bool = is_nsfw

    @property
    def app(self) -> PartialCommand | None:
        return self._app

    @app.setter
    def app(self, application: PartialCommand) -> None:
        self._app = application

    async def callback(self, context: InteractionContext) -> None:
        pass
