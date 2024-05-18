from __future__ import annotations

import asyncio
import typing
from logging import getLogger

from hikari.events import InteractionCreateEvent, StartedEvent, StartingEvent

from aurum.enum.sync_commands import SyncCommandsFlag
from aurum.ext.plugins import PluginManager
from aurum.internal.commands.app_command import AppCommand
from aurum.internal.commands.command_handler import CommandHandler
from aurum.internal.exceptions.base_exception import AurumException
from aurum.internal.interaction_processor import InteractionProcessor
from aurum.l10n.pass_localization_provider import PassLocalizationProvider

if typing.TYPE_CHECKING:
    from collections.abc import Coroutine, Sequence
    from logging import Logger

    from aurum.includable import Includable
    from aurum.l10n import LocalizationProviderInterface
    from aurum.types import BotT

__all__: Sequence[str] = ("Client",)


class Client:
    """A wrapper class for the main bot class, designed to work with the Aurum framework and its features.

    Note:
        At the moment, the wrapper only supports gateway connections.

    Attributes:
        l10n (LocalizationProviderInterface): The localization provider instance for multi-language support.
            It is recommended to provide a localization provider if multi-language support is required.
        bot (BotT): The bot instance.
        commands (CommandHandler): The command handler.
        plugins (PluginManager): The plugin manager.

    Args:
        bot (BotT): The bot instance that this client will interact with.
        sync_commands (SyncCommandFlag): An optional SyncCommandsFlag enum value, indicating how to handle command synchronization.
        l10n (LocalizationProviderInterface): Localization provider.
            If a localization provider is not provided, an `EmptyLocalizationProvider`
            will be used, which will pass all functions and return the key.
        ignore_l10n (bool): An optional flag. If `True`, the client will not emit a warning when a localization provider is not provided.
        ignore_unknown_interactions (bool): An optional flag that, if set to `True`, will disable the warning message for unknown interactions.
    """

    __slots__: Sequence[str] = (
        "l10n",
        "__logger",
        "_starting_tasks",
        "_sync_commands",
        "_interaction_processor",
        "bot",
        "commands",
        "plugins",
    )

    def __init__(
        self,
        bot: BotT,
        *,
        sync_commands: SyncCommandsFlag = SyncCommandsFlag.SYNC,
        l10n: LocalizationProviderInterface | None = None,
        ignore_l10n: bool = False,
        ignore_unknown_interactions: bool = False,
    ) -> None:
        self.__logger: Logger = getLogger("aurum.client")
        self._starting_tasks: typing.List[Coroutine[None, None, typing.Any]] = []
        self._sync_commands: SyncCommandsFlag = sync_commands

        if not l10n and not ignore_l10n:
            self.__logger.warning(
                "a localization provider has not been specified and localization will not be available. "
                "If you require localization, please use one of the available localization providers "
                "or create your own implementation based on the LocalizationProviderInterface."
            )
        self.l10n: LocalizationProviderInterface = l10n or PassLocalizationProvider()
        self.add_starting_task(self.l10n.start())

        self.bot: BotT = bot
        self.commands: CommandHandler = CommandHandler(bot, self.l10n)
        self.plugins: PluginManager = PluginManager(bot, self)
        self._interaction_processor: InteractionProcessor = InteractionProcessor(
            bot=bot,
            client=self,
            l10n=self.l10n,
            commands=self.commands,
            ignore_unknown_interactions=ignore_unknown_interactions,
            get_locale_func=self.l10n.get_locale,
        )

        for event, callback in {
            StartingEvent: self._on_starting,
            StartedEvent: self._on_started,
        }.items():
            self.bot.event_manager.subscribe(event, callback)  # type: ignore

    async def _on_starting(self, _: StartingEvent) -> None:
        try:
            await asyncio.gather(*self._starting_tasks)
            self.__logger.debug("completed all tasks")
        except Exception as exception:
            self.__logger.warning(
                "some tasks weren't completed because of an exception", exc_info=exception
            )

    async def _on_started(self, _: StartedEvent) -> None:
        if self._sync_commands.value:
            await self.commands.sync(debug=self._sync_commands == SyncCommandsFlag.DEBUG)
        self.bot.event_manager.subscribe(
            InteractionCreateEvent, self._interaction_processor.on_interaction
        )

    def add_starting_task(self, coro: Coroutine[None, None, typing.Any]) -> None:
        self._starting_tasks.append(coro)

    def include(self, includable: typing.Type[Includable]) -> None:
        if issubclass(includable, AppCommand):
            try:
                instance: AppCommand = includable()  # type: ignore
            except ValueError:
                raise AurumException("`__init__` of base includable wasn't overrided")
            self.commands.commands[instance.name] = instance
