from __future__ import annotations

import asyncio
import typing
from logging import getLogger

from hikari.events import InteractionCreateEvent, StartedEvent, StartingEvent

from aurum.enum.sync_commands import SyncCommandsFlag
from aurum.includable import Includable
from aurum.internal.commands.app_command import AppCommand
from aurum.internal.commands.command_handler import CommandHandler
from aurum.internal.interaction_processor import InteractionProcessor
from aurum.l10n import LocalizationProviderInterface

if typing.TYPE_CHECKING:
    from collections.abc import Coroutine, Sequence
    from logging import Logger

    from hikari.impl import GatewayBot

__all__: Sequence[str] = ("Client",)


class Client:
    """
    A wrapper class for the main bot class, designed to work with the Aurum framework and its features.

    At the moment, the wrapper only supports gateway connections.

    Attributes:
        bot (GatewayBot): The bot instance.
        l10n (LocalizationProviderInterface): The localization provider instance for multi-language support.
            It is recommended to provide a localization provider if multi-language support is required.
            You can use the our DefaultLocalizationProvider or create your own by inheriting from the LocalizationProviderInterface.

    Args:
        bot: The bot instance that this client will interact with.
        sync_commands: An optional SyncCommandsFlag enum value, indicating how to handle command synchronization.
        l10n: Localization provider.
            If a localization provider is not provided, an `EmptyLocalizationProvider` will be used, which will pass all functions and return the key.
        ignore_l10n: An optional boolean flag. If `True`, the client will not emit a warning when a localization provider is not provided.
        ignore_unknown_interactions: An optional boolean flag that, if set to `True`, will disable the warning message for unknown interactions.

    Examples:
        ```py
        bot = hikari.GatewayBot("...")
        l10n = MyCoolLocalizationProvider()
        client = Client(bot, l10n=l10n)
        ```
    """

    __slots__: Sequence[str] = (
        "__logger",
        "_starting_tasks",
        "_commands",
        "_interaction_processor",
        "_sync_commands",
        "bot",
        "l10n",
    )

    def __init__(
        self,
        bot: GatewayBot,
        *,
        sync_commands: SyncCommandsFlag = SyncCommandsFlag.SYNC,
        l10n: LocalizationProviderInterface | None = None,
        ignore_l10n: bool = False,
        ignore_unknown_interactions: bool = False,
    ) -> None:
        self.__logger: Logger = getLogger("aurum.client")
        self._starting_tasks: typing.List[Coroutine[None, None, typing.Any]] = []

        self.bot: GatewayBot = bot

        if not l10n and not ignore_l10n:
            self.__logger.warning(
                "A localization provider has not been specified and localization will not be available. "
                "If you require localization, please use one of the available localization providers "
                "or create your own implementation based on the LocalizationProviderInterface."
            )
        self.l10n: LocalizationProviderInterface = l10n or EmptyLocalizationProvider()
        self.add_starting_task(self.l10n.start())

        self._commands: CommandHandler = CommandHandler(bot, self.l10n)
        self._interaction_processor: InteractionProcessor = InteractionProcessor(
            bot=bot,
            client=self,
            l10n=self.l10n,
            commands=self._commands,
            components=None,
            ignore_unknown_interactions=ignore_unknown_interactions,
            get_locale_func=self.l10n.get_locale_from_interaction,
        )
        self._sync_commands: SyncCommandsFlag = sync_commands

        for event, callback in {
            StartingEvent: self._on_starting,
            StartedEvent: self._on_started,
        }.items():
            self.bot.event_manager.subscribe(event, callback)

    async def _on_starting(self, _: StartingEvent) -> None:
        try:
            await asyncio.gather(*self._starting_tasks)
            self.__logger.debug("Completed all tasks")
        except Exception as exception:
            self.__logger.warning(
                "Some tasks weren't completed because of an exception", exc_info=exception
            )

    async def _on_started(self, _: StartedEvent) -> None:
        if self._sync_commands.value:
            await self._commands.sync(debug=self._sync_commands == SyncCommandsFlag.DEBUG)
        self.bot.event_manager.subscribe(
            InteractionCreateEvent, self._interaction_processor.on_interaction
        )

    def add_starting_task(self, coro: Coroutine[None, None, typing.Any]) -> None:
        self._starting_tasks.append(coro)

    def include(self, includable: typing.Type[Includable]) -> None:
        if issubclass(includable, AppCommand):
            instance: AppCommand = includable()  # type: ignore
            self._commands.commands[instance.name] = instance


class EmptyLocalizationProvider(LocalizationProviderInterface): ...
