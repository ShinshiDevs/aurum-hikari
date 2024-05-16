from __future__ import annotations

import typing

from hikari.undefined import UNDEFINED
from hikari.permissions import Permissions

from aurum.includable import Includable

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

    from hikari.commands import CommandType, PartialCommand
    from hikari.guilds import PartialGuild
    from hikari.snowflakes import SnowflakeishOr
    from hikari.undefined import UndefinedType

    from aurum.interactions import InteractionContext
    from aurum.l10n.types import LocalizedOr


class AppCommand(Includable):
    """
    Represents a application command.

    !!! This class is not suitable for use, please use the pre-existing implementations.

    Attributes:
        _app (PartialCommand): Command application instance, available after sync.
        command_type (CommandType): Type of the command.
        name (str): The command name.
        description (LocalizedOr[str] | None): Optional description of the command for help documentation.
        guild (SnowflakeishOr[PartialGuild] | UndefinedType): Optional guild (server) where the command is available.
        default_member_permissions (Permissions): The permissions a user must have to use the command by default.
        dm_enabled (bool): Whether the command can be used in direct messages.
        is_nsfw (bool): Indicates whether the command is age-restricted.

    Args:
        name (str): The unique name of the command.
        description (LocalizedOr[str] | None): A description of command.
        display_name (LocalizedOr[str] | None): The localized name of the command.
        guild (SnowflakeishOr[PartialGuild] | UndefinedType): The guild in which the command is available.
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
        guild: SnowflakeishOr[PartialGuild] | UndefinedType = UNDEFINED,
        default_member_permissions: Permissions = Permissions.NONE,
        dm_enabled: bool = False,
        is_nsfw: bool = False,
    ) -> None:
        self._app: PartialCommand | None = None

        self.command_type: CommandType = command_type
        self.description: LocalizedOr[str] | None = description

        self.guild: SnowflakeishOr[PartialGuild] | UndefinedType = guild
        self.default_member_permissions: Permissions = default_member_permissions
        self.dm_enabled: bool = dm_enabled
        self.is_nsfw: bool = is_nsfw

        super().__init__(name=name)

    @property
    def app(self) -> PartialCommand | None:
        return self._app

    @app.setter
    def app(self, application: PartialCommand) -> None:
        self._app = application

    async def callback(self, context: InteractionContext) -> None:
        pass
