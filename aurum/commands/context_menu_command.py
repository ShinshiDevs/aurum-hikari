from collections.abc import Callable, Sequence

from hikari.api import ContextMenuCommandBuilder
from hikari.commands import CommandType
from hikari.guilds import PartialGuild
from hikari.permissions import Permissions
from hikari.snowflakes import SnowflakeishOr
from hikari.undefined import UNDEFINED, UndefinedType

from aurum.commands.app_command import AppCommand
from aurum.l10n import LocalizationProviderInterface
from aurum.l10n.localized import Localized
from aurum.l10n.types import LocalizedOr


class ContextMenuCommand(AppCommand):
    __slots__: Sequence[str] = (
        "app",
        "name",
        "display_name",
        "guild",
        "default_member_permissions",
        "dm_enabled",
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
        super().__init__(
            name=name,
            display_name=display_name,
            guild=guild,
            default_member_permissions=default_member_permissions,
            is_dm_enabled=is_dm_enabled,
            is_nsfw=is_nsfw,
        )

    def get_builder(
        self,
        factory: Callable[[CommandType | int, str], ContextMenuCommandBuilder],
        l10n: LocalizationProviderInterface | None,
    ) -> ContextMenuCommandBuilder:
        if l10n and isinstance(self.display_name, Localized):
            l10n.build_localized(self.display_name)
        builder = (
            factory(self.command_type, self.name)
            .set_name_localizations(
                localizations
                if isinstance(localizations := getattr(self.display_name, "value", {}), dict)
                else {}
            )
            .set_default_member_permissions(self.default_member_permissions)
            .set_is_dm_enabled(self.is_dm_enabled)
            .set_is_nsfw(self.is_nsfw)
        )
        return builder
