from __future__ import annotations

import asyncio
import typing
from collections.abc import Callable
from logging import getLogger

from hikari.commands import CommandType, OptionType
from hikari.events import InteractionCreateEvent, StartedEvent, StartingEvent
from hikari.interactions import CommandInteraction, ComponentInteraction

from aurum.client.integration import IClientIntegration
from aurum.commands import MessageCommand, SlashCommand, SubCommand, UserCommand
from aurum.enum.sync_commands import SyncCommandsFlag
from aurum.interactions import InteractionContext
from aurum.internal.commands.app_command import AppCommand
from aurum.internal.commands.command_handler import CommandHandler
from aurum.internal.exceptions import AurumException, UnknownCommandException
from aurum.l10n.pass_localization_provider import PassLocalizationProvider

if typing.TYPE_CHECKING:
    from collections.abc import Coroutine, Sequence
    from logging import Logger

    from hikari.interactions import (
        CommandInteractionOption,
        PartialInteraction,
    )

    from aurum.ext.plugins import PluginManager
    from aurum.includable import Includable
    from aurum.l10n import LocalizationProviderInterface
    from aurum.types import BotT


class Client:
    """A wrapper class for the main bot class, designed to work with the Aurum framework and its features.

    Note:
        At the moment, the wrapper only supports gateway connections.

    Attributes:
        l10n (LocalizationProviderInterface): The localization provider instance for multi-language support.
            It is recommended to provide a localization provider if multi-language support is required.
        bot (BotT): The bot instance.
        commands (CommandHandler): The command handler.

    Args:
        bot (BotT): The bot instance that this client will interact with.
        l10n (LocalizationProviderInterface): Localization provider.
            If a localization provider is not provided, an `EmptyLocalizationProvider`
            will be used, which will pass all functions and return the key.
        integrations: (Sequence[IClientIntegration]): A list of integrations for client.
        sync_commands (SyncCommandFlag): An optional SyncCommandsFlag enum value, indicating how to handle command synchronization.
        ignore_l10n (bool): An optional flag. If `True`, the client will not emit a warning when a localization provider is not provided.
        ignore_unknown_interactions (bool): An optional flag that, if set to `True`, will disable the warning message for unknown interactions.
    """

    __slots__: Sequence[str] = (
        "__logger",
        "_starting_tasks",
        "_sync_commands",
        "_ignore_unknown_interactions",
        "l10n",
        "bot",
        "commands",
        "plugins",
    )

    def __init__(
        self,
        bot: BotT,
        *,
        l10n: LocalizationProviderInterface | None = None,
        integrations: Sequence[IClientIntegration] = (),
        sync_commands: SyncCommandsFlag = SyncCommandsFlag.SYNC,
        ignore_l10n: bool = False,
        ignore_unknown_interactions: bool = False,
    ) -> None:
        self.__logger: Logger = getLogger("aurum.client")
        self._starting_tasks: typing.List[Coroutine[None, None, typing.Any]] = []
        self._sync_commands: SyncCommandsFlag = sync_commands
        self._ignore_unknown_interactions: bool = ignore_unknown_interactions

        self.l10n: LocalizationProviderInterface = l10n or PassLocalizationProvider()
        if not l10n and not ignore_l10n:
            self.__logger.warning(
                "a localization provider has not been specified and localization will not be available. "
                "If you require localization, please use one of the available localization providers "
                "or create your own implementation based on the LocalizationProviderInterface."
            )
        else:
            self.add_starting_task(self.l10n.start())

        self.bot: BotT = bot
        self.commands: CommandHandler = CommandHandler(bot, self.l10n)
        self.plugins: PluginManager | None = None

        for integration in integrations:
            integration.install(self)
            self.__logger.debug(f"installed integration: {type(integration).__qualname__}")

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
            self.__logger.debug("syncing commands")
            await self.commands.sync(debug=self._sync_commands == SyncCommandsFlag.DEBUG)
        self.bot.event_manager.subscribe(InteractionCreateEvent, self.on_interaction)

    def add_starting_task(self, coro: Coroutine[None, None, typing.Any]) -> None:
        """Add a starting task.

        Args:
            coro (Coroutine[None, None, typing.Any]): Any coroutine.
        """
        self._starting_tasks.append(coro)
        self.__logger.debug(f"add starting task: {coro.__qualname__}")

    def include(self, includable: typing.Type[Includable]) -> None:
        """Decorator to include an includable object to client"""
        if issubclass(includable, AppCommand):
            try:
                instance: AppCommand = includable()  # type: ignore
            except TypeError:
                raise AurumException("`__init__` of base includable wasn't overrided")
            self.commands.commands[instance.name] = instance

    def create_interaction_context(
        self, interaction: ComponentInteraction | CommandInteraction
    ) -> InteractionContext:
        return InteractionContext(
            interaction=interaction,
            bot=self.bot,
            client=self,
            locale=self.l10n.get_locale(interaction),
        )

    async def on_interaction(self, event: InteractionCreateEvent) -> None:
        interaction: PartialInteraction = event.interaction
        if isinstance(interaction, CommandInteraction):
            return await self.proceed_command(interaction)

    async def proceed_command(self, interaction: CommandInteraction) -> None:
        context: InteractionContext = self.create_interaction_context(interaction)
        parent_command: AppCommand | None = self.commands.commands.get(interaction.command_name)
        if not parent_command and not self._ignore_unknown_interactions:
            raise UnknownCommandException(interaction.command_name)
        command: AppCommand | SubCommand | None = parent_command
        if interaction.command_type is CommandType.SLASH:
            assert isinstance(command, SlashCommand)
            options: Sequence[CommandInteractionOption] | None = interaction.options
            arguments: typing.Dict[str, typing.Any] = {}
            if options:
                option: CommandInteractionOption = options[0]
                if option.type is OptionType.SUB_COMMAND:
                    command = command.sub_commands.get(option.name)
                    options = option.options
                    if not command and not self._ignore_unknown_interactions:
                        raise UnknownCommandException(option.name, interaction.command_name)
                elif option.type is OptionType.SUB_COMMAND_GROUP:
                    sub_command_group: SubCommand | None = command.sub_commands.get(option.name)
                    if not sub_command_group:
                        raise UnknownCommandException(option.name, interaction.command_name)
                    if options := option.options:
                        command = sub_command_group.sub_commands.get(options[0].name)
                        options = options[0].options
                        if not command and not self._ignore_unknown_interactions:
                            raise UnknownCommandException(
                                option.name, sub_command_group.name, interaction.command_name
                            )
                for option in options or ():
                    arguments[option.name] = context.resolve_command_argument(option)
            callback: Callable[..., Coroutine[None, None, typing.Any]] = getattr(
                command, "callback"
            )
            if isinstance(command, SlashCommand):
                await callback(context, **arguments)
                return
            await callback(parent_command, context, **arguments)
            return
        if interaction.command_type is CommandType.MESSAGE:
            assert isinstance(command, MessageCommand)
            assert interaction.resolved
            await command.callback(
                context,
                list(interaction.resolved.messages.values())[0],
            )
            return
        if interaction.command_type is CommandType.USER:
            assert isinstance(command, UserCommand)
            assert interaction.resolved
            await command.callback(
                context,
                list(interaction.resolved.users.values())[0],
            )
            return
