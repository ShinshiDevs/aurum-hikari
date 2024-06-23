from __future__ import annotations

import importlib.util
import inspect
import re
import typing
from collections.abc import Iterator, Sequence
from importlib.machinery import ModuleSpec
from logging import Logger, getLogger
from os import PathLike
from pathlib import Path

from hikari.api import CommandBuilder
from hikari.commands import PartialCommand
from hikari.guilds import PartialApplication, PartialGuild
from hikari.snowflakes import Snowflake, SnowflakeishOr
from hikari.traits import GatewayBotAware
from hikari.undefined import UndefinedType

from aurum.commands import MessageCommand, SlashCommand, UserCommand
from aurum.internal.commands.app_command import AppCommand
from aurum.internal.commands.context_menu_command import ContextMenuCommand
from aurum.internal.exceptions.base_exception import AurumException
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

        self._commands_builders: typing.Dict[
            SnowflakeishOr[PartialGuild] | UndefinedType, typing.Dict[str, CommandBuilder]
        ] = {}

        self.commands: typing.Dict[str, AppCommand] = {}
        self.app_commands: typing.Dict[Snowflake, AppCommand] = {}

    async def sync(self, debug: bool = False) -> None:
        """Synchronizes the builders of commands with the Discord API for the bot application.

        This method will handle both global commands and guild-specific commands,
        ensuring they are up-to-date with the currently stored command builders.

        Args:
            debug: A boolean flag that, when set to True, enables more verbose logging
                   of the synchronization process for debugging purposes.
            build: A boolean flag to enable a automatic building of commands.
        """
        if not self._app:
            self._app = await self._bot.rest.fetch_application()
        synchronized: typing.Dict[
            SnowflakeishOr[PartialGuild] | UndefinedType, Sequence[PartialCommand]
        ] = {}
        for command in self.commands.values():
            self._commands_builders.setdefault(command.guild, {})
            if builder := self.get_command_builder(command):
                self._commands_builders[command.guild][command.name] = builder
        for guild, builders in self._commands_builders.items():
            synchronized[guild] = await self._bot.rest.set_application_commands(
                self._app, list(builders.values()), guild=guild
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
        """Load commands from folder"""
        for file in Path(directory).rglob("*.py"):
            if re.compile("(^_.*|.*_$)").match(file.name):
                continue
            for command in self.load_commands_from_file(file):
                self.commands[command.name] = command
