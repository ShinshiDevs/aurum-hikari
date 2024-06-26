from __future__ import annotations

import asyncio
from collections.abc import Coroutine, Sequence
from logging import Logger, getLogger
from typing import Any, Dict, List

from hikari.commands import CommandType, OptionType
from hikari.errors import HikariError
from hikari.events import InteractionCreateEvent, StartedEvent, StartingEvent
from hikari.interactions import (
    CommandInteraction,
    CommandInteractionOption,
    ComponentInteraction,
    PartialInteraction,
)
from hikari.messages import Message
from hikari.snowflakes import Snowflake
from hikari.traits import GatewayBotAware
from hikari.users import User

from aurum.commands.enum import SyncCommandsFlag
from aurum.commands.typing import CommandCallbackT
from aurum.ext.plugins import PluginManager
from aurum.interactions import InteractionContext
from aurum.internal.commands.app_command import AppCommand
from aurum.internal.commands.command_handler import CommandHandler
from aurum.internal.exceptions import UnknownCommandException
from aurum.internal.includable import Includable
from aurum.l10n import LocalizationProviderInterface

__all__: Sequence[str] = ("Client",)


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
        self.__starting_tasks: List[Coroutine[None, None, Any]] = []

        self._sync_commands: SyncCommandsFlag = sync_commands
        self._ignore_unknown_interactions: bool = ignore_unknown_interactions

        self.bot: GatewayBotAware = bot
        self.l10n: LocalizationProviderInterface | None = l10n
        self.commands: CommandHandler = CommandHandler(bot, self.l10n)
        self.plugins: PluginManager = PluginManager(bot, self)

        self.bot.event_manager.subscribe(StartingEvent, self.on_starting)
        self.bot.event_manager.subscribe(StartedEvent, self.on_started)

        if not l10n and not ignore_l10n:
            self.__logger.warning(
                "a localization provider has not been specified and localization will not be available. "
                "If you require localization, please use one of the available localization providers "
                "or create your own implementation based on the LocalizationProviderInterface."
            )
        else:
            self.__starting_tasks.append(l10n.start())

    async def on_starting(self, _: StartingEvent) -> None:
        completed: Sequence[Any | Exception] = await asyncio.gather(
            *self.__starting_tasks, return_exceptions=True
        )
        for result in completed:
            if isinstance(result, Exception):
                self.__logger.exception("Task raised exception", exc_info=result)

    async def on_started(self, _: StartedEvent) -> None:
        if self._sync_commands.value:
            self.__logger.debug("syncing commands")
            await self.commands.sync(debug=self._sync_commands == SyncCommandsFlag.DEBUG)
        self.bot.event_manager.subscribe(InteractionCreateEvent, self.on_interaction)

    async def add_starting_task(self, coro: Coroutine[None, None, Any]) -> None:
        self.__starting_tasks.append(coro)

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
        command: AppCommand | None = self.commands.app_commands.get(interaction.command_id)

        try:
            if interaction.command_type in (CommandType.USER, CommandType.MESSAGE):
                resolved: Dict[Snowflake, User | Message] = (
                    interaction.resolved.users  # interaction.resolved is weird thing actually, but it's not our care
                    if interaction.command_type is CommandType.USER
                    else interaction.resolved.messages
                )  # type: ignore
                await command.callback(
                    context, tuple(resolved.values())[0]
                )  # type of command must be UserCommand or MessageCommand
                return

            callback: CommandCallbackT | None = None
            arguments: Dict[str, Any] = {}
            options: Sequence[CommandInteractionOption] = interaction.options or ()

            if (callback := getattr(command, "callback", None)) and not command.sub_commands:
                for option in options:
                    arguments[option.name] = context.resolve_command_argument(option)
                return await callback(context, **arguments)

            for option in options:
                if option.type is OptionType.SUB_COMMAND:
                    if sub_command := command.sub_commands.get(option.name):
                        options = option.options or ()
                        callback = sub_command.callback
                if option.type is OptionType.SUB_COMMAND_GROUP:
                    if sub_command_group := command.sub_commands.get(option.name):
                        options = option.options or ()
                        for option in options:
                            if sub_command := sub_command_group.sub_commands.get(option.name):
                                options = option.options or ()
                                callback = sub_command.callback
            if callback:
                for option in options:
                    arguments[option.name] = context.resolve_command_argument(option)
                # command required, because it's must be a sub_command because of decorator, sub command don't see parent command class (self)
                await callback(command, context, **arguments)
                return
        except UnknownCommandException:
            raise
        except Exception as error:
            return await self.on_unexcepted_error(context, error)

    async def on_unexcepted_error(self, context: InteractionContext, error: Exception) -> None:
        """Response on unexcepted error"""
        self.__logger.error("exception occurred while command proceeding", exc_info=error)
        try:
            await context.create_response("An unexcepted error occurred.", ephemeral=True)
        except HikariError:
            await context.edit_response("An unexcepted error occurred.")
        return

    async def on_command_error(self, context: InteractionContext, error: Exception) -> None:
        """Handler of commands' errors"""
        await self.on_unexcepted_error(context, error)

    def include(self, includable: typing.Type[Includable]) -> None:
        """Decorator to include an includable object to client"""
        if issubclass(includable, AppCommand):
            instance: AppCommand = includable()  # type: ignore
            self.commands.commands[instance.name] = instance
