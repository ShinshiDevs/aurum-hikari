from __future__ import annotations

import importlib.util
import inspect
import re
from collections.abc import Iterator, Sequence
from importlib.machinery import ModuleSpec
from logging import Logger, getLogger
from os import PathLike
from pathlib import Path
from typing import Dict, List

from hikari import AutocompleteInteraction
from hikari.api import CommandBuilder as APICommandBuilder
from hikari.commands import CommandType, OptionType, PartialCommand
from hikari.guilds import PartialApplication, PartialGuild
from hikari.interactions import CommandInteraction, CommandInteractionOption
from hikari.snowflakes import SnowflakeishOr
from hikari.traits import GatewayBotAware
from hikari.undefined import UndefinedType

from aurum.commands import MessageCommand, SlashCommand, UserCommand
from aurum.commands.app_command import AppCommand
from aurum.commands.context_menu_command import ContextMenuCommand
from aurum.commands.sub_command import SubCommand
from aurum.context import AutocompleteContext, InteractionContext
from aurum.exceptions import AurumException
from aurum.internal.command_builder import CommandBuilder
from aurum.l10n import LocalizationProviderInterface

CommandsTypes = MessageCommand, SlashCommand, UserCommand


class CommandHandler:
    """Handles command building and synchronization for a bot application.

    This class is responsible for application commands.
    It registers commands, synchronizes them with the Discord API.

    Attributes:
        commands (Dict[str, AppCommand]): Dictionary that stores the AppCommand instances, keyed by their names.
        app_commands (Dict[Snowflake, AppCommand]): Dictionary that stores AppCommand instances, keyed by their application ID
    """

    __slots__: Sequence[str] = (
        "__logger",
        "app",
        "bot",
        "l10n",
        "builder",
        "builders_dict",
        "commands",
        "app_commands",
    )

    def __init__(
        self, bot: GatewayBotAware, l10n: LocalizationProviderInterface | None = None
    ) -> None:
        self.__logger: Logger = getLogger("aurum.commands")

        self.bot: GatewayBotAware = bot
        self.l10n: LocalizationProviderInterface | None = l10n
        self.builder: CommandBuilder = CommandBuilder(bot, self, l10n)

        self.app: PartialApplication | None = None
        self.commands: Dict[str, AppCommand] = {}

    async def sync(self, *, debug: bool = False) -> None:
        """Synchronizes the builders of commands with the Discord API for the bot application.

        This method will handle both global commands and guild-specific commands.

        Args:
            debug: A boolean flag that, when set to True, enables more verbose logging
                   of the synchronization process for debugging purposes.
        """
        self.__logger.info("synchronizing commands...")

        if self.app is None:
            self.app = await self.bot.rest.fetch_application()

        guilds: Dict[SnowflakeishOr[PartialGuild] | UndefinedType, List[AppCommand]] = {}
        for command in self.commands.values():
            guilds.setdefault(command.guild, [])
            guilds[command.guild].append(command)

        for guild, commands in guilds.items():
            assert self.app is not None
            app_commands: Sequence[PartialCommand] = await self.bot.rest.set_application_commands(
                self.app,
                list(map(self.get_builder, commands)),
                guild=guild,
            )
            for command in app_commands:
                self.commands[command.name].set_app(command)
            self.__logger.info("set commands for %s", guild)

            if debug:
                debug_log = "\n".join(
                    f"- {command.name} {command.app.id} ({command})"
                    for command in self.commands.values()
                    if command.app
                )
                self.__logger.debug("commands for %s:\n%s", guild, debug_log)

        self.__logger.info("synchronized successfully")

    def get_builder(
        self, command: AppCommand | SlashCommand | ContextMenuCommand
    ) -> APICommandBuilder:
        assert isinstance(command, (SlashCommand, ContextMenuCommand))
        return {
            CommandType.SLASH: self.builder.get_slash_command,
            CommandType.MESSAGE: self.builder.get_context_menu_command,
            CommandType.USER: self.builder.get_context_menu_command,
        }[command.command_type](command)

    def get_command(
        self, context: InteractionContext | AutocompleteContext
    ) -> SlashCommand | ContextMenuCommand | SubCommand:
        """Get command from context.

        Because sub-commands are passed through the `options` field of the received interaction,
        the arguments for the command have already been processed and are located
        in the `context.arguments` field (`InteractionContext.arguments`).
        """
        assert isinstance(context.interaction, (CommandInteraction, AutocompleteInteraction))
        
        command: AppCommand | SubCommand | None = self.commands.get(
            context.interaction.command_name
        )

        if isinstance(command, ContextMenuCommand):
            return command

        elif isinstance(command, SlashCommand):
            options: List[CommandInteractionOption] = list(context.interaction.options or [])

            while options:
                option: CommandInteractionOption = options.pop()

                if option.type in (OptionType.SUB_COMMAND, OptionType.SUB_COMMAND_GROUP):
                    assert isinstance(command, (SlashCommand, SubCommand))
                    command = command.sub_commands.get(option.name, None)
                    options = list(option.options or [])
                elif not isinstance(context, AutocompleteContext):
                    context.arguments[option.name] = context.resolve_command_argument(option)

            assert isinstance(command, (SlashCommand, SubCommand))
            return command
        else:
            raise

    def load_commands_from_file(self, file: Path) -> Iterator[AppCommand]:
        spec: ModuleSpec | None = importlib.util.spec_from_file_location(file.name, file)
        if not spec or not getattr(spec, "loader", None):
            raise
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, CommandsTypes) and obj not in CommandsTypes:
                try:
                    yield obj()  # type: ignore
                except TypeError:
                    raise AurumException("`__init__` of base includable wasn't overrided")

    def load_folder(self, directory: PathLike[str]) -> None:
        """Load commands from folder."""
        for file in Path(directory).rglob("*.py"):
            if re.compile("(^_.*|.*_$)").match(file.name):
                continue
            for command in self.load_commands_from_file(file):
                self.commands[command.name] = command
