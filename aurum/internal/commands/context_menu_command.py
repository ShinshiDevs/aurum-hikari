from collections.abc import Callable, Sequence

from hikari.api import ContextMenuCommandBuilder
from hikari.commands import CommandType
from hikari.guilds import PartialGuild
from hikari.permissions import Permissions
from hikari.snowflakes import SnowflakeishOr
from hikari.undefined import UNDEFINED, UndefinedType

from aurum.internal.commands.app_command import AppCommand
from aurum.l10n import LocalizationProviderInterface


class ContextMenuCommand(AppCommand):
    __slots__: Sequence[str] = (
        "app",
        "name",
        "guild",
        "default_member_permissions",
        "dm_enabled",
        "is_nsfw",
    )

    def __init__(
        self,
        name: str,
        *,
        guild: SnowflakeishOr[PartialGuild] | UndefinedType = UNDEFINED,
        default_member_permissions: Permissions = Permissions.NONE,
        is_dm_enabled: bool = False,
        is_nsfw: bool = False,
    ) -> None:
        super().__init__(
            name=name,
            guild=guild,
            default_member_permissions=default_member_permissions,
            is_dm_enabled=is_dm_enabled,
            is_nsfw=is_nsfw,
        )

    def get_builder(
        self,
        factory: Callable[[CommandType | int, str], ContextMenuCommandBuilder],
        l10n: LocalizationProviderInterface,  # type: ignore  # TODO: display name
    ) -> ContextMenuCommandBuilder:
        builder = (
            factory(self.command_type, self.name)
            .set_default_member_permissions(self.default_member_permissions)
            .set_is_dm_enabled(self.is_dm_enabled)
            .set_is_nsfw(self.is_nsfw)
        )
        return builder
