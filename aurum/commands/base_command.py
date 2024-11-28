from collections.abc import Sequence

from hikari.commands import CommandType
from hikari.guilds import PartialGuild
from hikari.permissions import Permissions
from hikari.snowflakes import SnowflakeishOr

from aurum.commands.types import Localized

__all__: Sequence[str] = ("BaseCommand",)


class BaseCommand:
    """Base class for Discord application command.

    Parameters
    ----------
    name : str
        The name of the command.
    name_localizations : Localized | None, optional
        The localizations of the command name.
    default_member_permissions : Permissions | None, optional
        Default permissions required to use this command.

        Members without these permissions won't see the command.
    is_dm_enabled : bool, default False
        Whether command can be used in DMs.
    is_nsfw : bool, default False
        Whether command is NSFW.
    guild_id : SnowflakeishOr[PartialGuild] | None, optional
        Guild ID if command is guild-specific.

    Attributes
    ----------
    type : CommandType
        Type of the command.
    """

    __slots__: Sequence[str] = (
        "_name",
        "_name_localizations",
        "_default_member_permissions",
        "_is_dm_enabled",
        "_is_nsfw",
        "_guild_id",
    )
    _command_type: CommandType

    def __init__(
        self,
        name: str,
        *,
        name_localizations: Localized | None = None,
        default_member_permissions: Permissions | None = None,
        is_dm_enabled: bool = False,
        is_nsfw: bool = False,
        guild_id: SnowflakeishOr[PartialGuild] | None = None,
    ) -> None:
        self._name: str = name
        self._name_localizations: Localized | None = name_localizations
        self._default_member_permissions: Permissions | None = default_member_permissions
        self._is_dm_enabled: bool = is_dm_enabled
        self._is_nsfw: bool = is_nsfw
        self._guild_id: SnowflakeishOr[PartialGuild] | None = guild_id

    @property
    def type(self) -> CommandType:
        return self._command_type

    @property
    def name(self) -> str:
        return self._name

    @property
    def name_localizations(self) -> Localized | None:
        return self._name_localizations

    @property
    def default_member_permissions(self) -> Permissions | None:
        return self._default_member_permissions

    @property
    def is_dm_enabled(self) -> bool:
        return self._is_dm_enabled

    @property
    def is_nsfw(self) -> bool:
        return self._is_nsfw

    @property
    def guild_id(self) -> SnowflakeishOr[PartialGuild] | None:
        return self._guild_id

    @name_localizations.setter
    def name_localizations(self, value: Localized | None) -> None:
        self._name_localizations = value

    @default_member_permissions.setter
    def default_member_permissions(self, value: Permissions | None) -> None:
        self._default_member_permissions = value

    @is_dm_enabled.setter
    def is_dm_enabled(self, value: bool) -> None:
        self._is_dm_enabled = value

    @is_nsfw.setter
    def is_nsfw(self, value: bool) -> None:
        self._is_nsfw = value

    @guild_id.setter
    def guild_id(self, value: SnowflakeishOr[PartialGuild] | None) -> None:
        self._guild_id = value
