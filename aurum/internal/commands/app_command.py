from __future__ import annotations

from collections.abc import Sequence

from hikari.commands import CommandType, PartialCommand
from hikari.guilds import PartialGuild
from hikari.permissions import Permissions
from hikari.snowflakes import SnowflakeishOr
from hikari.undefined import UNDEFINED, UndefinedType

from aurum.internal.includable import Includable
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
        "app",
        "name",
        "display_name",
        "guild",
        "default_member_permissions",
        "is_dm_enabled",
        "is_nsfw",
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
        self.app: PartialCommand | None = None

        self.display_name: LocalizedOr[str] | None = display_name

        self.guild: SnowflakeishOr[PartialGuild] | UndefinedType = guild
        self.default_member_permissions: Permissions = default_member_permissions
        self.is_dm_enabled: bool = is_dm_enabled
        self.is_nsfw: bool = is_nsfw

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
