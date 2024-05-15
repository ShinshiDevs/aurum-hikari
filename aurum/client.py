from __future__ import annotations

import typing
from asyncio import create_task
from logging import getLogger

from hikari.events import InteractionCreateEvent, StartedEvent, StartingEvent

from aurum.commands.command_handler import CommandHandler
from aurum.enum.sync_commands import SyncCommandsFlag
from aurum.interactions.interaction_processor import InteractionProcessor

if typing.TYPE_CHECKING:
    from asyncio.tasks import Task
    from collections.abc import Coroutine, Sequence
    from logging import Logger

    from hikari.impl import GatewayBot

    from aurum.l10n import LocalizationProviderInterface


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
        self._starting_tasks: typing.List[Task[typing.Any]] = []

        self._commands: CommandHandler = CommandHandler()
        self._interaction_processor: InteractionProcessor = InteractionProcessor(
            bot, self._commands, None, ignore_unknown_interactions
        )
        self._sync_commands: SyncCommandsFlag = sync_commands

        self.bot: GatewayBot = bot

        if not l10n and not ignore_l10n:
            self.__logger.warn(
                "A localization provider has not been specified and localization will not be available. "
                "If you require localization, please use one of the available localization providers "
                "or create your own implementation based on the LocalizationProviderInterface."
            )
        self.l10n: LocalizationProviderInterface = l10n or EmptyLocalizationProvider()
        self.add_starting_task(self.l10n.start(), name=str(self.l10n))

        for event, callback in {
            StartingEvent: self._on_starting,
            StartedEvent: self._on_started,
        }.items():
            self.bot.event_manager.subscribe(event, callback)

    async def _on_starting(self, _: StartingEvent) -> None:
        for task in self._starting_tasks:
            try:
                await task
            except Exception as exception:
                self.__logger.warn(
                    "Task %s wasn't completed, because of exception",
                    task.get_name(),
                    exc_info=exception,
                )
                continue
        self.__logger.debug("Completed all tasks")

    async def _on_started(self, _: StartedEvent) -> None:
        if self._sync_commands.value:
            await self._commands.sync(debug=self._sync_commands is SyncCommandsFlag.DEBUG)
        self.bot.event_manager.subscribe(
            InteractionCreateEvent, self._interaction_processor.on_interaction
        )

    def add_starting_task(
        self, coro: Coroutine[None, None, typing.Any], *, name: str | None = None
    ) -> None:
        self._starting_tasks.append(create_task(coro, name=name))


class EmptyLocalizationProvider(LocalizationProviderInterface): ...
