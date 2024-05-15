from __future__ import annotations

import typing
from logging import getLogger

from hikari.undefined import UNDEFINED

if typing.TYPE_CHECKING:
    from collections.abc import Sequence
    from logging import Logger

    from hikari.commands import PartialCommand
    from hikari.guilds import PartialApplication, PartialGuild
    from hikari.impl import CommandBuilder, GatewayBot
    from hikari.snowflakes import SnowflakeishOr
    from hikari.undefined import UndefinedType

    from aurum.commands.app_command import AppCommand


class CommandHandler:
    """Handles command building and synchronization for a bot application.

    This class is responsible for application commands.
    It registers commands, synchronizes them with the Discord API.
    
    Attributes:
        commands (typing.Dict[str, AppCommand]): Dictionary that stores the actual AppCommand instances, keyed by their names.
    
    Args:
        bot (GatewayBot): A bot instance.

    Methods:
        sync: Sync commands with the Discord API.
        get_command: 
            Get command.

            Returns:
                AppCommand
                None: If command wasn't found
    """

    __slots__: Sequence[str] = (
        "__logger",
        "_app",
        "_bot",
        "_commands_builders",
        "commands",
    )

    def __init__(self, bot: GatewayBot) -> None:
        self.__logger: Logger = getLogger("aurum.commands")
        self._app: PartialApplication | None = None
        self._bot: GatewayBot = bot
        self._commands_builders: typing.Dict[
            SnowflakeishOr[PartialGuild] | UndefinedType, typing.Dict[str, CommandBuilder]
        ] = {}

        self.commands: typing.Dict[str, AppCommand] = {}

    async def sync(self, debug: bool = False) -> None:
        """
        Synchronizes the builders of commands with the Discord API for the bot application.

        This method will handle both global commands and guild-specific commands,
        ensuring they are up-to-date with the currently stored command builders.
        
        Args:
            debug: A boolean flag that, when set to True, enables more verbose logging 
                   of the synchronization process for debugging purposes.
        """
        synchronized: typing.Dict[
            SnowflakeishOr[PartialGuild] | UndefinedType, Sequence[PartialCommand]
        ] = {}
        if not self._app:
            self._app = await self._bot.rest.fetch_application()
        synchronized[UNDEFINED] = await self._bot.rest.set_application_commands(
            self._app, list(self._commands_builders.pop(UNDEFINED).values())
        )
        for guild, commands_builders in self._commands_builders.items():
            synchronized[guild] = await self._bot.rest.set_application_commands(
                self._app, list(commands_builders.values()), guild=guild
            )
        for entity, commands in synchronized.items():
            for command in commands:
                self.commands[command.name]._app = command
            if debug:
                self.__logger.debug(
                    "Set commands for %s: %s",
                    entity,
                    ", ".join(command.name for command in commands),
                )

    def get_command(
        self,
        command_name: str,
        *,
        group_name: str | None = None,
        subgroup_name: str | None = None,
    ) -> AppCommand | None: 
        command: AppCommand | None = None
        return command
