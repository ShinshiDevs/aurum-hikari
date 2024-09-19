from __future__ import annotations

from collections.abc import Sequence

from hikari.commands import CommandType, PartialCommand
from hikari.guilds import PartialGuild
from hikari.permissions import Permissions
from hikari.snowflakes import SnowflakeishOr
from hikari.undefined import UNDEFINED, UndefinedType

from aurum.includable import Includable
from aurum.l10n.types import LocalizedOr


class AppCommand(Includable):
    """Represents an application command.

    Attributes:
        app (PartialCommand): Command application instance, available after sync.
        name (str): The command name.
        display_name (LocalizedOr[str] | None): A display name of command.
            Can be localized.
        guild (SnowflakeishOr[PartialGuild] | UndefinedType): An optional guild (server) where the command is available.
        default_member_permissions (Permissions): The permissions a user must have to use the command by default.
        dm_enabled (bool): Whether the command can be used in direct messages.
        is_nsfw (bool): Indicates whether the command is age-restricted.
    """

    command_type: CommandType

    __slots__: Sequence[str] = (
        "_app",
        "_name",
        "_display_name",
        "_guild",
        "_default_member_permissions",
        "_is_dm_enabled",
        "_is_nsfw",
    )

    def __init__(
        self,
        name: str,
        *,
        display_name: LocalizedOr[str] | None = None,
        guild: SnowflakeishOr[PartialGuild] | UndefinedType = UNDEFINED,
        default_member_permissions: Permissions = Permissions.NONE,
        is_dm_enabled: bool = False,
        is_nsfw: bool = False,
    ) -> None:
        super().__init__(name=name)
        self._app: PartialCommand | None = None

        self._display_name: LocalizedOr[str] | None = display_name

        self._guild: SnowflakeishOr[PartialGuild] | UndefinedType = guild
        self._default_member_permissions: Permissions = default_member_permissions
        self._is_dm_enabled: bool = is_dm_enabled
        self._is_nsfw: bool = is_nsfw

    @property
    def app(self) -> PartialCommand | None:
        return self._app

    @app.setter
    def app(self, app: PartialCommand) -> None:
        self._app = app

    @property
    def guild(self) -> SnowflakeishOr[PartialGuild] | UndefinedType:
        return self._guild

    @guild.setter
    def guild(self, guild: SnowflakeishOr[PartialGuild] | UndefinedType) -> None:
        self._guild = guild

    @property
    def default_member_permissions(self) -> Permissions:
        return self._default_member_permissions

    @default_member_permissions.setter
    def default_member_perimssions(self, permissions: Permissions) -> None:
        self._default_member_permissions = permissions

    @property
    def is_dm_enabled(self) -> bool:
        return self._is_dm_enabled

    @is_dm_enabled.setter
    def is_dm_enabled(self, is_dm_enabled: bool) -> None:
        self._is_dm_enabled = is_dm_enabled

    @property
    def is_nsfw(self) -> bool:
        return self._is_nsfw

    @is_nsfw.setter
    def is_nsfw(self, is_nsfw: bool) -> None:
        self._is_nsfw = is_nsfw
