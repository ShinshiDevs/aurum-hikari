from typing import Dict, List, TypeVar

from hikari.applications import Application
from hikari.commands import CommandType, PartialCommand
from hikari.impl import CommandBuilder, GatewayBot
from hikari.interactions import CommandInteraction
from hikari.snowflakes import Snowflakeish
from hikari.undefined import UNDEFINED, UndefinedType

from aurum.commands.slash_command import SlashCommand as AurumSlashCommand

GLOBAL = TypeVar("GLOBAL")


class CommandHandler:
    def __init__(self) -> None:
        self.slash_commands: Dict[str, AurumSlashCommand] = {}

        self._commands_builders: Dict[
            Snowflakeish | UndefinedType, Dict[str, CommandBuilder]
        ] = {}

    async def sync(self, bot: GatewayBot) -> None:
        self._commands_builders = self.get_commands_builders()
        application: Application = await bot.rest.fetch_application()
        app_commands: List[PartialCommand] = []
        app_commands.extend(
            await bot.rest.set_application_commands(
                application,
                list(self._commands_builders[UNDEFINED].values()),
            )
        )
        for guild, commands in self._commands_builders.items():
            if guild is not UNDEFINED:
                app_commands.extend(
                    await bot.rest.set_application_commands(
                        application,
                        list(commands.values()),
                    )
                )
        for command in app_commands:
            match command.type:
                case CommandType.SLASH:
                    self.slash_commands[command.name].app = command

    async def process(self, interaction: CommandInteraction) -> None: ...

    def get_commands_builders(
        self,
    ) -> Dict[Snowflakeish | UndefinedType, Dict[str, CommandBuilder]]: ...
