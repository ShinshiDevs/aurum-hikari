from __future__ import annotations

import importlib.util
import re
from collections.abc import Sequence
from importlib.machinery import ModuleSpec
from logging import Logger, getLogger
from os import PathLike
from pathlib import Path
from types import ModuleType
from typing import TYPE_CHECKING, Dict

from hikari.traits import GatewayBotAware

from aurum.ext.plugins.plugin import Plugin
from aurum.internal.commands.app_command import AppCommand
from aurum.internal.commands.command_handler import CommandHandler

if TYPE_CHECKING:
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

        self.plugins: Dict[str, Plugin] = {}

    def load_plugin_from_file(self, file: PathLike[str]) -> Plugin | None:
        """Load plugin from file

        File must have a `plugin` variable
        """
        file = Path(file)
        if not file.is_file():
            return None
        spec: ModuleSpec | None = importlib.util.spec_from_file_location(file.stem, file)
        if not spec or not getattr(spec, "loader", None):
            return None
        module: ModuleType = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
            plugin: Plugin | None = getattr(module, "plugin", None)
            if isinstance(plugin, Plugin):
                return plugin(self._bot, self._client)
            self.__logger.warning(
                "plugin in %s is not detected.",
                file,
            )
        except Exception as exception:
            self.__logger.error("couldn't load file %s due error", file, exc_info=exception)
        return None

    async def load_folder(self, directory: PathLike[str], *, recursive: bool = True) -> None:
        """Load plugins from folder"""
        path: Path = Path(directory)
        for file in (path.rglob if recursive else path.glob)("*.py"):
            plugin: Plugin | None = self.load_plugin_from_file(file)
            if not plugin or re.compile("(^_.*|.*_$)").match(file.name):
                continue
            for includable in plugin.included.values():
                if isinstance(includable, AppCommand):
                    self._commands.commands[includable.name] = includable
            self.__logger.debug("loaded %s", plugin.name)
