from __future__ import annotations

import importlib.util
import re
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

    from hikari.traits import GatewayBotAware

    from aurum.client import Client


class PluginManager:
    """Plugin manager.

    Attributes:
        plugins (Dict[str, Plugin]): A dictionary of loaded plugins, keyed by their names.
    """

    __slots__: Sequence[str] = ("__logger", "_bot", "_client", "_commands", "plugins")

    def __init__(self, bot: GatewayBotAware, client: Client) -> None:
        self.__logger: Logger = getLogger("aurum.plugins")

        self._bot: GatewayBotAware = bot
        self._client: Client = client
        self._commands: CommandHandler = client.commands

        self.plugins: typing.Dict[str, Plugin] = {}

    def load_plugin_from_file(self, file: PathLike[str]) -> Plugin | None:
        """Load plugin from file

        File must have a `plugin` variable
        """
        file = Path(file) if not isinstance(file, Path) else file
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
                return plugin(self._bot, self._client)
            self.__logger.error(
                "plugin in %s is not not detected.",
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
            if re.compile("(^_.*|.*_$)").match(file.name):
                continue
            plugin: Plugin | None = self.load_plugin_from_file(file)
            if not plugin:
                return
            for includable in plugin.included.values():
                if isinstance(includable, AppCommand):
                    self._commands.commands[includable.name] = includable
            loaded.append(plugin)
        self.__logger.debug("loaded %s", ", ".join([plugin.name for plugin in loaded]))
