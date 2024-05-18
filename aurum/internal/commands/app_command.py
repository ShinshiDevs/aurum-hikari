from __future__ import annotations

import typing

from hikari.permissions import Permissions
from hikari.undefined import UNDEFINED

from aurum.includable import Includable

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

    from hikari.commands import CommandType, PartialCommand
    from hikari.guilds import PartialGuild
    from hikari.snowflakes import SnowflakeishOr
    from hikari.undefined import UndefinedType

    from aurum.l10n.types import LocalizedOr


class AppCommand(Includable):
    """Represents an application command.

    !!! This class is not suitable for use, please use the pre-existing implementations.

    Attributes:
        app (PartialCommand): Command application instance, available after sync.
        command_type (CommandType): Type of the command.
        name (str): The command name.
        description (LocalizedOr[str] | None): Optional description of the command for help documentation.
        guild (SnowflakeishOr[PartialGuild] | UndefinedType): Optional guild (server) where the command is available.
        default_member_permissions (Permissions): The permissions a user must have to use the command by default.
        dm_enabled (bool): Whether the command can be used in direct messages.
        is_nsfw (bool): Indicates whether the command is age-restricted.
    """

    __slots__: Sequence[str] = (
        "_app",
        "_name",
        "_display_name",
        "_guild",
        "_default_member_permissions",
        "_is_dm_enabled",
        "_is_nsfw",
        "description",
        "command_type",
    )

    def __init__(
        self,
        command_type: CommandType,
        name: str,
        description: LocalizedOr[str] | None = None,
        *,
        guild: SnowflakeishOr[PartialGuild] | UndefinedType = UNDEFINED,
        default_member_permissions: Permissions = Permissions.NONE,
        is_dm_enabled: bool = False,
        is_nsfw: bool = False,
    ) -> None:
        super().__init__(name=name)

        self._app: PartialCommand | None = None

        self._guild: SnowflakeishOr[PartialGuild] | UndefinedType = guild

        self._default_member_permissions: Permissions = default_member_permissions
        self._is_dm_enabled: bool = is_dm_enabled
        self._is_nsfw: bool = is_nsfw

        self.description: LocalizedOr[str] | None = description
        self.command_type: CommandType = command_type

    @property
    def app(self) -> PartialCommand | None:
        return self._app

    @app.setter
    def app(self, application: PartialCommand) -> None:
        self._app = application

    @property
    def guild(self) -> SnowflakeishOr[PartialGuild] | UndefinedType:
        return self._guild

    @guild.setter
    def guild(self, guild: SnowflakeishOr[PartialGuild]) -> None:
        self._guild = guild

    @property
    def default_member_permissions(self) -> Permissions:
        return self._default_member_permissions

    @default_member_permissions.setter
    def default_member_permissions(self, permissions: Permissions) -> None:
        self._default_member_permissions = permissions

    @property
    def is_dm_enabled(self) -> bool:
        return self._is_dm_enabled

    @is_dm_enabled.setter
    def is_dm_enabled(self, dm_enabled: bool) -> None:
        self._is_dm_enabled = dm_enabled

    @property
    def is_nsfw(self) -> bool:
        return self._is_nsfw

    @is_nsfw.setter
    def is_nsfw(self, nsfw: bool) -> None:
        self._is_nsfw = nsfw
