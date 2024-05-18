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
        description (LocalizedOr[str] | None): An optional description of the command.
        guild (SnowflakeishOr[PartialGuild] | UndefinedType): An optional guild (server) where the command is available.
        default_member_permissions (Permissions): The permissions a user must have to use the command by default.
        dm_enabled (bool): Whether the command can be used in direct messages.
        is_nsfw (bool): Indicates whether the command is age-restricted.
    """

    __slots__: Sequence[str] = (
        "app",
        "name",
        "display_name",
        "guild",
        "default_member_permissions",
        "is_dm_enabled",
        "is_nsfw",
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
        self.app: PartialCommand | None = None

        self.guild: SnowflakeishOr[PartialGuild] | UndefinedType = guild

        self.default_member_permissions: Permissions = default_member_permissions
        self.is_dm_enabled: bool = is_dm_enabled
        self.is_nsfw: bool = is_nsfw

        self.description: LocalizedOr[str] | None = description
        self.command_type: CommandType = command_type

    def set_app(self, application: PartialCommand) -> AppCommand:
        self.app = application
        return self

    def set_guild(self, guild: SnowflakeishOr[PartialGuild] | UndefinedType) -> AppCommand:
        self.guild = guild
        return self

    def set_default_member_permissions(self, permissions: Permissions) -> AppCommand:
        self.default_member_permissions = permissions
        return self

    def set_is_dm_enabled(self, dm_enabled: bool) -> AppCommand:
        self.is_dm_enabled = dm_enabled
        return self

    def set_is_nsfw(self, nsfw: bool) -> AppCommand:
        self.is_nsfw = nsfw
        return self
