from collections.abc import Sequence

from hikari.guilds import PartialGuild
from hikari.permissions import Permissions
from hikari.snowflakes import SnowflakeishOr
from hikari.undefined import UNDEFINED, UndefinedType

from aurum.commands.app_command import AppCommand
from aurum.hooks import Hook
from aurum.l10n.types import LocalizedOr


class ContextMenuCommand(AppCommand):
    __slots__: Sequence[str] = ("display_name", "dm_enabled", "hooks")

    def __init__(
        self,
        name: str,
        *,
        display_name: LocalizedOr[str] | None = None,
        guild: SnowflakeishOr[PartialGuild] | UndefinedType = UNDEFINED,
        default_member_permissions: Permissions = Permissions.NONE,
        is_dm_enabled: bool = False,
        is_nsfw: bool = False,
        hooks: Sequence[Hook] = (),
    ) -> None:
        super().__init__(
            name=name,
            display_name=display_name,
            guild=guild,
            default_member_permissions=default_member_permissions,
            is_dm_enabled=is_dm_enabled,
            is_nsfw=is_nsfw,
        )
        self.hooks: Sequence[Hook] = hooks
