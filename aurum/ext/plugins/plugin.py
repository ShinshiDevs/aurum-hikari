from __future__ import annotations

import typing

from hikari.permissions import Permissions
from hikari.undefined import UNDEFINED

from aurum.includable import Includable
from aurum.internal.commands.app_command import AppCommand
from aurum.internal.exceptions.base_exception import AurumException

if typing.TYPE_CHECKING:
    from hikari.guilds import PartialGuild
    from hikari.snowflakes import SnowflakeishOr
    from hikari.undefined import UndefinedType

    from aurum.client import Client
    from aurum.l10n import LocalizedOr
    from aurum.types import BotT


class Plugin:
    def __init__(
        self,
        name: str,
        description: LocalizedOr[str] | None = None,
        *,
        guild: SnowflakeishOr[PartialGuild] | UndefinedType = UNDEFINED,
        default_member_permissions: Permissions = Permissions.NONE,
        is_dm_enabled: bool = False,
        is_nsfw: bool = False,
    ) -> None:
        self._bot: BotT | None = None
        self._client: Client | None = None

        self.name: str = name
        self.description: LocalizedOr[str] | None = description

        self.guild: SnowflakeishOr[PartialGuild] | UndefinedType = guild
        self.default_member_permissions: Permissions = default_member_permissions
        self.is_dm_enabled: bool = is_dm_enabled
        self.is_nsfw: bool = is_nsfw

        self.included: typing.Dict[str, Includable] = {}

    def include(self, includable: typing.Type[Includable]) -> None:
        if issubclass(includable, AppCommand):
            try:
                instance: AppCommand = (
                    includable()  # type: ignore
                    .set_guild(self.guild)
                    .set_default_member_permissions(self.default_member_permissions)
                    .set_is_dm_enabled(self.is_dm_enabled)
                    .set_is_nsfw(self.is_nsfw)
                )
            except ValueError:
                raise AurumException("`__init__` of base includable wasn't overrided")
            self.included[instance.name] = instance
