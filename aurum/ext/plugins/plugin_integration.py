from __future__ import annotations

import typing
from pathlib import Path

from aurum.client.integration import IClientIntegration
from aurum.ext.plugins.plugin_manager import PluginManager

if typing.TYPE_CHECKING:
    from os import PathLike

    from aurum.client import Client


class PluginIntegration(IClientIntegration):
    """Plugins integration

    Plugin integration adds to client `plugins` variable with manager.

    Args:
        plugin_manager (Type[PluginManager]): An optional class of plugin manager.
            Plugin integration initialize plugin manager yourself.
        base_directory (PathLike[str]): An optional base directory with plugins.
            If a base directory is specified, the integration will automatically add a task to load the specified folder.

    Example:
        ```py
        client = Client(
            bot,
            integrations=[
                PluginIntegration(base_directory=Path("bot", "plugins")) # (1)
            ]
        )
        ```
        { .annotate }

        1. If a base directory is specified, the integration will automatically add a task to load the specified folder.
    """

    def __init__(
        self,
        plugin_manager: typing.Type[PluginManager] = PluginManager,
        *,
        base_directory: PathLike[str] | None = None,
    ):
        self.plugin_manager: typing.Type[PluginManager] = plugin_manager
        self.base_directory: Path | None = Path(base_directory) if base_directory else None

    def install(self, client: Client) -> None:
        client.plugins = self.plugin_manager(client.bot, client)
        if self.base_directory:
            client.add_starting_task(client.plugins.load_folder(self.base_directory))
