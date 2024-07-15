from __future__ import annotations

import sys
from asyncio import iscoroutine
from collections.abc import Callable, Coroutine, Sequence
from logging import Logger, getLogger
from typing import Any, Type, overload

from hikari import AutocompleteInteractionOption
from hikari.events import InteractionCreateEvent, StartedEvent, StartingEvent
from hikari.interactions import (
    AutocompleteInteraction,
    CommandInteraction,
    ComponentInteraction,
    PartialInteraction,
)
from hikari.traits import GatewayBotAware

from aurum.autocomplete import AutocompleteChoice
from aurum.commands import MessageCommand, SlashCommand, SubCommand, UserCommand
from aurum.commands.app_command import AppCommand
from aurum.commands.context_menu_command import ContextMenuCommand
from aurum.commands.enum import SyncCommandsFlag
from aurum.context import AutocompleteContext, InteractionContext
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
            self.add_starting_task(l10n.start())  # type: ignore

        self.bot.event_manager.subscribe(StartedEvent, self.on_started)
        self.bot.event_manager.subscribe(InteractionCreateEvent, self.on_interaction)

    async def on_started(self, _: StartedEvent) -> None:
        if self._sync_commands.value:
            await self.commands.sync(debug=self._sync_commands == SyncCommandsFlag.DEBUG)

    def add_starting_task(
        self, task: Callable[..., Any] | Coroutine[None, None, Any], **kwargs: Any
    ) -> None:
        """Add starting task.

        With coroutine function: `Client.add_starting_task(coroutine_function(...))`
        With sync function: `Client.add_starting_task(some_function, integer=956)` or `Client.add_starting_task(labmda: some_function(956))`
        """

        async def callback(_: StartingEvent) -> None:
            if iscoroutine(task):
                return await task
            return task(**kwargs)

        self.bot.event_manager.subscribe(StartingEvent, callback)

    @overload
    def create_context(
        self, interaction: CommandInteraction | ComponentInteraction
    ) -> InteractionContext: ...

    @overload
    def create_context(self, interaction: AutocompleteInteraction) -> AutocompleteContext: ...

    def create_context(
        self, interaction: ComponentInteraction | CommandInteraction | AutocompleteInteraction
    ) -> InteractionContext | AutocompleteContext:
        if isinstance(interaction, (CommandInteraction, ComponentInteraction)):
            return InteractionContext(
                interaction=interaction,
                bot=self.bot,
                client=self,
                locale=self.l10n.get_locale(interaction) if self.l10n else None,
            )
        else:
            return AutocompleteContext(
                interaction=interaction,
                bot=self.bot,
                client=self,
                locale=self.l10n.get_locale(interaction) if self.l10n else None,
            )

    async def on_interaction(self, event: InteractionCreateEvent) -> None:
        interaction: PartialInteraction = event.interaction
        if isinstance(interaction, CommandInteraction):
            return await self.proceed_command(interaction)
        if isinstance(interaction, AutocompleteInteraction):
            return await self.proceed_autocomplete(interaction)

    async def proceed_command(self, interaction: CommandInteraction) -> None:
        context: InteractionContext = self.create_context(interaction)
        command: CommandT = self.commands.get_command(context)
        try:
            for hook in command.hooks:
                if (await hook.callback(context)).stop:
                    return
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
                    command.parent,  # type: ignore
                    context,
                    **context.arguments,
                )
        except Exception as error:
            exc_info = sys.exc_info()
            if not self.bot.event_manager.get_listeners(CommandErrorEvent):
                return self.__logger.error(
                    "unhandled command %s error", command.name, exc_info=exc_info
                )
            self.bot.event_manager.dispatch(
                CommandErrorEvent(
                    app=self.bot,
                    client=self,
                    exc_info=exc_info,  # type: ignore
                    exception=error,
                    command=command,  # type: ignore
                    interaction=interaction,
                    context=context,
                )
            )

    async def proceed_autocomplete(self, interaction: AutocompleteInteraction) -> None:
        context: AutocompleteContext = self.create_context(interaction)
        command: CommandT = self.commands.get_command(context)
        option: AutocompleteInteractionOption = interaction.options[0]
        for interaction_option in interaction.options:
            if isinstance(command, SlashCommand):
                option = interaction_option
            if isinstance(command, SubCommand):
                for interaction_option in interaction_option.options or ():
                    option = interaction_option
        assert isinstance(command, (SlashCommand, SubCommand))
        if (autocomplete := command.autocompletes[option.name]) and option.is_focused:
            assert autocomplete.autocomplete
            choices: Sequence[AutocompleteChoice] = await autocomplete.autocomplete(context, option)
            await interaction.create_response(list(choice.to_builder() for choice in choices))

    def include(self, includable: Type[Includable]) -> None:
        """Decorator to include an includable object to client."""
        if issubclass(includable, AppCommand):
            instance: AppCommand = includable()  # type: ignore
            self.commands.commands[instance.name] = instance
