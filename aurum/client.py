from __future__ import annotations

import sys
from collections.abc import Coroutine, Sequence
from logging import Logger, getLogger
from typing import Any, Type

from hikari.events import InteractionCreateEvent, StartedEvent, StartingEvent
from hikari.interactions import (
    CommandInteraction,
    ComponentInteraction,
    PartialInteraction,
)
from hikari.traits import GatewayBotAware

from aurum.commands import MessageCommand, SlashCommand, SubCommand, UserCommand
from aurum.commands.app_command import AppCommand
from aurum.commands.context_menu_command import ContextMenuCommand
from aurum.commands.enum import SyncCommandsFlag
from aurum.context import InteractionContext
from aurum.events import CommandErrorEvent
from aurum.ext.plugins import PluginManager
from aurum.internal.command_handler import CommandHandler
from aurum.internal.includable import Includable
from aurum.l10n import LocalizationProviderInterface

__all__: Sequence[str] = ("Client",)

CommandT = SlashCommand | ContextMenuCommand | SubCommand


class Client:
    """A wrapper class for the main bot class, designed to work with the Aurum framework and its features.

    Note:
        At the moment, the wrapper only supports gateway connections.

    Attributes:
        bot (GatewayBotAware): The bot instance.
        l10n (LocalizationProviderInterface): The localization provider instance for multi-language support.
            It is recommended to provide a localization provider if multi-language support is required.
        commands (CommandHandler): The command handler.
        plugins (PluginManager): The plugins manager.

    Args:
        bot (GatewayBotAware): The bot instance that this client will interact with.
        l10n (LocalizationProviderInterface): Localization provider.
            If a localization provider is not provided, an `EmptyLocalizationProvider`
            will be used, which will pass all functions and return the key.
        sync_commands (SyncCommandFlag): An optional SyncCommandsFlag enum value, indicating how to handle command synchronization.
        ignore_l10n (bool): An optional flag. If `True`, the client will not emit a warning when a localization provider is not provided.
        ignore_unknown_interactions (bool): An optional flag that, if set to `True`, will disable the warning message for unknown interactions.
    """

    __slots__: Sequence[str] = (
        "__logger",
        "__starting_tasks",
        "_sync_commands",
        "_ignore_unknown_interactions",
        "bot",
        "l10n",
        "commands",
        "plugins",
    )

    def __init__(
        self,
        bot: GatewayBotAware,
        *,
        l10n: LocalizationProviderInterface | None = None,
        sync_commands: SyncCommandsFlag = SyncCommandsFlag.SYNC,
        ignore_l10n: bool = False,
        ignore_unknown_interactions: bool = False,
    ) -> None:
        self.__logger: Logger = getLogger("aurum.client")

        self._sync_commands: SyncCommandsFlag = sync_commands
        self._ignore_unknown_interactions: bool = ignore_unknown_interactions

        self.bot: GatewayBotAware = bot

        self.l10n: LocalizationProviderInterface | None = l10n
        self.commands: CommandHandler = CommandHandler(bot, self.l10n)
        self.plugins: PluginManager = PluginManager(bot, self)

        if not l10n and not ignore_l10n:
            self.__logger.warning(
                "a localization provider has not been specified and localization will not be available. "
                "If you require localization, please use one of the available localization providers "
                "or create your own implementation based on the LocalizationProviderInterface."
            )
        else:
            self.add_starting_task(l10n.start())

        self.bot.event_manager.subscribe(StartedEvent, self.on_started)
        self.bot.event_manager.subscribe(InteractionCreateEvent, self.on_interaction)

    async def on_started(self, _: StartedEvent) -> None:
        if self._sync_commands.value:
            await self.commands.sync(debug=self._sync_commands == SyncCommandsFlag.DEBUG)

    def add_starting_task(self, coro: Coroutine[None, None, Any]) -> None:
        """Add starting task."""

        async def callback(_: StartingEvent) -> None:
            await coro

        self.bot.event_manager.subscribe(StartingEvent, callback)

    def create_interaction_context(
        self, interaction: ComponentInteraction | CommandInteraction
    ) -> InteractionContext:
        return InteractionContext(
            interaction=interaction,
            bot=self.bot,
            client=self,
            locale=self.l10n.get_locale(interaction) if self.l10n else None,
        )

    async def on_interaction(self, event: InteractionCreateEvent) -> None:
        interaction: PartialInteraction = event.interaction
        if isinstance(interaction, CommandInteraction):
            return await self.proceed_command(interaction)

    async def proceed_command(self, interaction: CommandInteraction) -> None:
        context: InteractionContext = self.create_interaction_context(interaction)
        command: CommandT = self.commands.get_command(context)
        try:
            if isinstance(command, SlashCommand):
                if not (callback := getattr(command, "callback", None)):
                    raise
                return await callback(context, **context.arguments)
            elif isinstance(command, UserCommand):
                return await command.callback(context, *interaction.resolved.users.values())  # type: ignore
            elif isinstance(command, MessageCommand):
                return await command.callback(context, *interaction.resolved.messages.values())  # type: ignore
            elif isinstance(command, SubCommand):
                return await command.callback(
                    self.commands.app_commands.get(context.interaction.command_id, None),  # type: ignore
                    context,
                    **context.arguments,
                )
        except Exception as error:
            self.bot.event_manager.dispatch(
                CommandErrorEvent(
                    app=self.bot,
                    client=self,
                    exc_info=sys.exc_info(),  # type: ignore
                    exception=error,
                    command=command,  # type: ignore
                    context=context,
                )
            )
            raise

    def include(self, includable: Type[Includable]) -> None:
        """Decorator to include an includable object to client."""
        if issubclass(includable, AppCommand):
            instance: AppCommand = includable()  # type: ignore
            self.commands.commands[instance.name] = instance
