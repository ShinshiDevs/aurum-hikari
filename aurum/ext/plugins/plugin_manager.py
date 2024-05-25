from __future__ import annotations

import importlib.util
import typing
from logging import getLogger
from pathlib import Path

from aurum.ext.plugins.plugin import Plugin
from aurum.internal.commands.app_command import AppCommand
from aurum.internal.commands.command_handler import CommandHandler

if typing.TYPE_CHECKING:
    from collections.abc import Sequence
    from importlib.machinery import ModuleSpec
    from logging import Logger
    from os import PathLike
    from types import ModuleType

    from aurum.client import Client
    from aurum.types import BotT


class PluginManager:
    """Plugin manager.

    Attributes:
        bot (BotT): The bot instance.
        client (Client): The client.
        commands (CommandHandler): The command handler.
        plugins (Dict[str, Plugin]): A dictionary of loaded plugins, keyed by their names.
    """

    __slots__: Sequence[str] = ("__logger", "bot", "client", "commands", "plugins")

    def __init__(self, bot: BotT, client: Client) -> None:
        self.__logger: Logger = getLogger("aurum.plugins")

        self.bot: BotT = bot
        self.client: Client = client

        self.commands: CommandHandler = client.commands

        self.plugins: typing.Dict[str, Plugin] = {}

    def load_plugin_from_file(self, file: PathLike[str]) -> Plugin | None:
        """Load plugin from file

        File must have a `plugin` variable
        """
        if not isinstance(file, Path):
            file = Path(file)
        if not file.is_file():
            return None
        module_name: str = file.stem
        spec: ModuleSpec | None = importlib.util.spec_from_file_location(module_name, file)
        if not spec:
            self.__logger.error("count not load module %s from %s.", module_name, file)
            return None
        module: ModuleType = importlib.util.module_from_spec(spec)
        try:
            if not spec.loader:
                self.__logger.error(
                    "cannot execute module %s from spec, because spec don't have loader.",
                    module_name,
                )
                return None
            spec.loader.exec_module(module)
            plugin: Plugin | None = getattr(module, "plugin", None)
            if isinstance(plugin, Plugin):
                plugin.bot = self.bot
                plugin.client = self.client
                return plugin
            self.__logger.error(
                "variable `plugin` in %s is not an instance of Plugin class or not detected.",
                file,
            )
        except Exception as exception:
            self.__logger.error(
                "couldn't load module %s due error", module_name, exc_info=exception
            )
            return None
        return None

    async def load_folder(self, directory: PathLike[str]) -> None:
        """Load plugins from folder"""
        loaded: typing.List[Plugin] = []
        for file in Path(directory).rglob("*.py"):
            plugin: Plugin | None = self.load_plugin_from_file(file)
            if not plugin:
                return
            plugin.bot = self.bot
            plugin.client = self.client
            for includable in plugin.included.values():
                if isinstance(includable, AppCommand):
                    self.commands.commands[includable.name] = includable
            loaded.append(plugin)
        self.__logger.debug("loaded %s", ", ".join([plugin.name for plugin in loaded]))
