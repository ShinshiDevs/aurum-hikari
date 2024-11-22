from __future__ import annotations

import inspect
from collections.abc import Sequence
from typing import TYPE_CHECKING

from hikari.commands import CommandType
from hikari.guilds import PartialGuild
from hikari.permissions import Permissions
from hikari.snowflakes import SnowflakeishOr

from aurum.commands.base_command import BaseCommand
from aurum.commands.exceptions import CommandCallbackNotImplemented
from aurum.commands.options import Option
from aurum.commands.sub_command import SubCommandMethod
from aurum.commands.types import Localized

if TYPE_CHECKING:
    from aurum.commands.types import CommandCallbackT


class SlashCommand(BaseCommand):
    """A class representing a slash command.

    Parameters
    ----------
    name : str
        The name of the command
    callback : CommandCallbackT | None, optional
        The callback function to be executed when command is invoked
    name_localizations : Localized | None, optional
        The command name localizations.
    description : str | None, optional
        The description of the command.
    description_localizations : Localized | None, optional
        The command description localizations.
    options : Sequence[Option] | None, optional
        The command options
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
    description : str | None
        The command description.
    description_localizations : Localized | None
        The command description localizations.
    options : Sequence[Option] | None
        The command options.
    """

    __slots__: Sequence[str] = (
        "_callback",
        "_name_localizations",
        "_description",
        "_description_localizations",
        "_options",
    )
    _command_type: CommandType = CommandType.SLASH

    def __init__(
        self,
        name: str,
        *,
        callback: CommandCallbackT | None = None,
        name_localizations: Localized | None = None,
        description: str | None = None,
        description_localizations: Localized | None = None,
        options: Sequence[Option] | None = None,
        default_member_permissions: Permissions | None = None,
        is_dm_enabled: bool = False,
        is_nsfw: bool = False,
        guild_id: SnowflakeishOr[PartialGuild] | None = None,
    ) -> None:
        super().__init__(
            name=name,
            name_localizations=name_localizations,
            default_member_permissions=default_member_permissions,
            is_dm_enabled=is_dm_enabled,
            is_nsfw=is_nsfw,
            guild_id=guild_id,
        )
        self._callback: CommandCallbackT | None = callback or getattr(self, "callback", None)
        if self._callback is None:
            raise CommandCallbackNotImplemented(self.name)

        self._description: str | None = description
        self._description_localizations: Localized | None = description_localizations
        self._options: Sequence[Option] | None = options

    @property
    def description(self) -> str | None:
        return self._description

    @property
    def description_localizations(self) -> Localized | None:
        return self._description_localizations

    @property
    def options(self) -> Sequence[Option] | None:
        return self._options


class SlashCommandGroup(BaseCommand):
    """A class representing a group of slash commands.

    Parameters
    ----------
    name : str
        The name of the command group.
    name_localizations : Localized | None, optional
        The command group name localizations.
    default_member_permissions : Permissions | None, optional
        Default permissions required to use commands in this group.

        Members without these permissions won't see the commands.
    is_dm_enabled : bool, default False
        Whether commands can be used in DMs.
    is_nsfw : bool, default False
        Whether commands are NSFW.
    guild_id : SnowflakeishOr[PartialGuild] | None, optional
        Guild ID if command is guild-specific.

    Attributes
    ----------
    sub_commands : Dict[str, SubCommandMethod]
        Dictionary mapping sub-command names to their methods.
    """

    __slots__: Sequence[str] = ("_sub_commands",)
    _command_type: CommandType = CommandType.SLASH

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
        super().__init__(
            name=name,
            name_localizations=name_localizations,
            default_member_permissions=default_member_permissions,
            is_dm_enabled=is_dm_enabled,
            is_nsfw=is_nsfw,
            guild_id=guild_id,
        )
        self._sub_commands: dict[str, SubCommandMethod] = {}

    @property
    def sub_commands(self) -> dict[str, SubCommandMethod]:
        return self._sub_commands

    def get_sub_commands(self) -> dict[str, SubCommandMethod]:
        if not self._sub_commands:
            for _, attr_value in inspect.getmembers(self):
                if isinstance(attr_value, SubCommandMethod):
                    sub_command = attr_value.command
                    self._sub_commands[sub_command.name] = attr_value
        return self._sub_commands
