from __future__ import annotations

import importlib.util
import inspect
import re
from collections.abc import Iterator, Sequence
from importlib.machinery import ModuleSpec
from logging import Logger, getLogger
from os import PathLike
from pathlib import Path
from typing import Dict

from hikari.api import CommandBuilder
from hikari.commands import OptionType, PartialCommand
from hikari.guilds import PartialApplication, PartialGuild
from hikari.interactions import CommandInteraction, CommandInteractionOption
from hikari.snowflakes import Snowflake, SnowflakeishOr
from hikari.traits import GatewayBotAware
from hikari.undefined import UndefinedType

from aurum.commands import MessageCommand, SlashCommand, UserCommand
from aurum.commands.app_command import AppCommand
from aurum.commands.context_menu_command import ContextMenuCommand
from aurum.commands.sub_command import SubCommand
from aurum.context import InteractionContext
from aurum.exceptions import AurumException
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
        "_app",
        "_bot",
        "_l10n",
        "_commands_builders",
        "commands",
        "app_commands",
    )

    def __init__(self, bot: GatewayBotAware, l10n: LocalizationProviderInterface) -> None:
        self.__logger: Logger = getLogger("aurum.commands")

        self._app: PartialApplication | None = None
        self._bot: GatewayBotAware = bot
        self._l10n: LocalizationProviderInterface = l10n

        self._commands_builders: Dict[
            SnowflakeishOr[PartialGuild] | UndefinedType, Dict[str, CommandBuilder]
        ] = {}

        self.commands: Dict[str, AppCommand] = {}
        self.app_commands: Dict[Snowflake, AppCommand] = {}

    async def sync(self, *, debug: bool = False) -> None:
        """Synchronizes the builders of commands with the Discord API for the bot application.

        This method will handle both global commands and guild-specific commands,
        ensuring they are up-to-date with the currently stored command builders.

        Args:
            debug: A boolean flag that, when set to True, enables more verbose logging
                   of the synchronization process for debugging purposes.
        """
        if not self._app:
            self._app = await self._bot.rest.fetch_application()
        synchronized: Dict[
            SnowflakeishOr[PartialGuild] | UndefinedType, Sequence[PartialCommand]
        ] = {}
        for command in self.commands.values():
            self._commands_builders.setdefault(command.guild, {})
            if builder := self.get_command_builder(command):
                self._commands_builders[command.guild][command.name] = builder
        for guild, builders in self._commands_builders.items():
            synchronized[guild] = await self._bot.rest.set_application_commands(
                self._app, builders.values(), guild=guild
            )
        for entity, commands in synchronized.items():
            for partial_command in commands:
                self.commands[partial_command.name].set_app(partial_command)
                self.app_commands[partial_command.id] = self.commands[partial_command.name]
            if debug:
                self.__logger.debug(
                    "Set commands for %s: %s",
                    entity,
                    ", ".join(command.name for command in commands),
                )

    def get_command(
        self, context: InteractionContext
    ) -> SlashCommand | ContextMenuCommand | SubCommand:
        """Get command from context.

        Because sub-commands are passed through the `options` field of the received interaction,
        the arguments for the command have already been processed and are located
        in the `context.arguments` field (`InteractionContext.arguments`).
        """
        assert isinstance(context.interaction, CommandInteraction)
        options: Sequence[CommandInteractionOption] = context.interaction.options or ()
        command: AppCommand | SubCommand | None = self.app_commands.get(
            context.interaction.command_id
        )
        # there's SubCommand type only because soon this variable will be used and for sub command too
        if isinstance(command, ContextMenuCommand):
            return command
        elif isinstance(command, SlashCommand):
            if command.sub_commands and not any(
                option.type in (OptionType.SUB_COMMAND, OptionType.SUB_COMMAND_GROUP)
                for option in options
            ):
                raise AurumException(
                    "Something seems to be wrong. Your command has subcommands, but we didn't receive any subcommands from the interaction. "
                    "Please check your command and the logs, and let us know if you want."
                )
            if not command.sub_commands:
                for option in options:
                    context.arguments[option.name] = context.resolve_command_argument(option)
                return command
            for option in options:
                if option.type is OptionType.SUB_COMMAND:
                    if sub_command := command.sub_commands.get(option.name):
                        options = option.options or ()
                        command = sub_command
                if option.type is OptionType.SUB_COMMAND_GROUP:
                    if sub_command_group := command.sub_commands.get(option.name):
                        options = option.options or ()
                        for option in options:
                            if sub_command := sub_command_group.sub_commands.get(option.name):
                                options = option.options or ()
                                command = sub_command
                for option in options:
                    context.arguments[option.name] = context.resolve_command_argument(option)
            return command
        else:
            raise

    def get_command_builder(self, command: AppCommand) -> CommandBuilder | None:
        if isinstance(command, SlashCommand):
            return command.get_builder(
                self._bot.rest.slash_command_builder,
                self._l10n,
            )
        elif isinstance(command, ContextMenuCommand):
            return command.get_builder(
                self._bot.rest.context_menu_command_builder,
                self._l10n,
            )
        return None

    def load_commands_from_file(self, file: Path) -> Iterator[AppCommand]:
        spec: ModuleSpec | None = importlib.util.spec_from_file_location(file.name, file)
        if not spec or not getattr(spec, "loader", None):
            raise
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for _, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, CommandsTypes) and obj not in CommandsTypes:
                # TODO!: Rewrite load_commands_from_file and Plugin part too
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
