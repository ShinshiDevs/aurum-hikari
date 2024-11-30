from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence
from logging import Logger, getLogger
from typing import TYPE_CHECKING

from hikari.api import special_endpoints as api
from hikari.applications import Application
from hikari.commands import OptionType, PartialCommand
from hikari.errors import BadRequestError
from hikari.events.interaction_events import InteractionCreateEvent
from hikari.events.lifetime_events import StartedEvent, StoppingEvent
from hikari.guilds import PartialGuild
from hikari.impl.gateway_bot import GatewayBot
from hikari.interactions import CommandInteraction, CommandInteractionOption
from hikari.snowflakes import SnowflakeishOr

from aurum.commands.base_command import BaseCommand
from aurum.commands.context_menu_command import MessageCommand, UserCommand
from aurum.commands.exceptions import CommandCallbackNotImplemented, CommandNotFound, SubCommandNotFound
from aurum.commands.impl.command_builder import CommandBuilder
from aurum.commands.slash_command import SlashCommand, SlashCommandGroup
from aurum.commands.sub_command import SubCommandMethod
from aurum.commands.utils.command_tree import build_command_tree
from aurum.commands.utils.resolve_interaction_option import resolve_interaction_option
from aurum.context import InteractionContext
from aurum.utils.logs import trace
from aurum.utils.timeit import timeit

if TYPE_CHECKING:
    from aurum.commands.types import CommandCallbackT, CommandMapping

__all__: Sequence[str] = ("CommandHandler",)


class CommandHandler:
    """This class handles the registration, synchronization, and execution of Discord commands.

    Parameters
    ----------
    bot : GatewayBot
        The Discord bot instance this handler will work with.
    sync_commands : bool, optional
        Whether to automatically sync commands on startup, by default False.

    Attributes
    ----------
    bot : GatewayBot
        The Discord bot instance.
    sync_commands_flag : bool
        Whether commands should be synced on startup.
    commands : Dict[str, BaseCommand]
        Mapping of command names to command instances.
    global_commands : CommandMapping
        Mapping of global command IDs to command instances.
    guild_commands : Dict[SnowflakeishOr[PartialGuild], CommandMapping]
        Mapping of guild IDs to their command mappings.
    """

    __slots__: Sequence[str] = (
        "__logger",
        "__application",
        "bot",
        "verbose",
        "sync_commands_flag",
        "commands",
        "global_commands",
        "guild_commands",
        "_commands_builders",
        "_builder",
    )

    def __init__(self, bot: GatewayBot, *, sync_commands: bool = False) -> None:
        self.__logger: Logger = getLogger("aurum.commands")
        self.__application: Application | None = None

        self.bot: GatewayBot = bot
        self.bot.event_manager.subscribe(StartedEvent, self.start)
        self.bot.event_manager.subscribe(StoppingEvent, self.stop)
        self.bot.event_manager.subscribe(InteractionCreateEvent, self.on_command_interaction)

        self.sync_commands_flag: bool = sync_commands

        self.commands: dict[str, BaseCommand] = {}
        self.global_commands: CommandMapping = {}
        self.guild_commands: dict[SnowflakeishOr[PartialGuild], CommandMapping] = defaultdict()
        # CommandMapping is MutableMapping[Snowflakeish, BaseCommand]
        # where Snowflakeish is command ID, BaseCommand is instance
        # of command in framework

        self._builder: CommandBuilder = CommandBuilder()
        self._commands_builders: dict[BaseCommand, api.CommandBuilder] = {}

    def create_context(self, interaction: CommandInteraction) -> InteractionContext:
        """Create a new interaction context from a command interaction.

        Parameters
        ----------
        interaction : CommandInteraction
            The command interaction to create the context from.

        Returns
        -------
        InteractionContext
            The created interaction context.
        """
        return InteractionContext(interaction=interaction, bot=self.bot)

    async def start(self, _: StartedEvent) -> None:
        """Start the command handler.

        This method initializes the command handler when the bot starts. If `sync_commands_flag`
        is True, it will fetch the application data and synchronize all registered commands.
        """
        self.__logger.debug("starting")
        async with timeit(self.__logger.debug, "started in %.2f seconds"):
            if self.sync_commands_flag is True:
                self.__logger.debug("syncing commands")
                self.__application = await self.bot.rest.fetch_application()
                self._commands_builders = self._builder.build_commands(self.bot, self.commands)
                await self.sync_commands()

    async def stop(self, _: StoppingEvent) -> None:
        """Stop the command handler.

        This method cleans up the command handler when the bot is stopping. It unsubscribes
        from events and clears all command registrations.
        """
        self.__logger.debug("stopping")
        self.bot.event_manager.unsubscribe(StartedEvent, self.start)
        self.bot.event_manager.unsubscribe(StoppingEvent, self.stop)
        self.bot.event_manager.unsubscribe(InteractionCreateEvent, self.on_command_interaction)
        self.commands.clear()
        self.global_commands.clear()
        self.guild_commands.clear()
        self._commands_builders.clear()

    async def sync_commands(self) -> None:
        """Synchronize the application commands with Discord.

        This method handles the synchronization of both global and guild-specific commands
        with Discord's API. It processes the registered commands and updates them on Discord's end.

        The synchronization process includes:
        1. Separating commands into global and guild-specific collections.
        2. Synchronizing guild-specific commands for each guild.
        3. Synchronizing global commands.

        Notes
        -----
            Requires the application to be initialized before calling
        """
        assert isinstance(self.__application, Application)

        global_commands: dict[BaseCommand, api.CommandBuilder] = {}
        guilds_commands: dict[SnowflakeishOr[PartialGuild], dict[BaseCommand, api.CommandBuilder]] = defaultdict(dict)
        self.__logger.info("starting command synchronization with %s commands", len(self.commands))

        async with timeit(self.__logger.info, "command synchronization completed in %.2f seconds"):
            for command, builder in self._commands_builders.items():
                if command.guild_id:
                    guilds_commands[command.guild_id][command] = builder
                else:
                    global_commands[command] = builder

            for guild, commands in guilds_commands.items():
                self.__logger.debug("syncing %d commands for guild %s", len(commands), guild)
                try:
                    response: Sequence[PartialCommand] = await self.bot.rest.set_application_commands(
                        self.__application, tuple(commands.values()), guild=guild
                    )
                except BadRequestError as error:
                    self.__logger.error("failed to set application commands for guild %s", exc_info=error)
                    continue
                self.guild_commands.setdefault(guild, {})
                for command in response:
                    self.guild_commands[guild][command.id] = self.commands[command.name]
                trace("guild %s commands tree: \n%s", guild, build_command_tree(response))
                self.__logger.info("%d commands synchronized for guild %s successfully", len(response), guild)

            self.__logger.debug("syncing %d global commands", len(global_commands))
            try:
                response: Sequence[PartialCommand] = await self.bot.rest.set_application_commands(
                    self.__application, tuple(global_commands.values())
                )
            except BadRequestError as error:
                self.__logger.error("failed to sync global commands", exc_info=error)
                return
            for command in response:
                self.global_commands[command.id] = self.commands[command.name]
            trace("global commands tree: \n%s", build_command_tree(response))
            self.__logger.info("%d global commands synchronized successfully", len(response))

    async def execute_command(self, interaction: CommandInteraction, command: BaseCommand) -> None:
        """Execute a Discord command based on the interaction and command type.

        Parameters
        ----------
        interaction : CommandInteraction
            The interaction event triggered by the command.
        command : BaseCommand
            The command instance to execute.
        """
        context: InteractionContext = self.create_context(interaction)

        if isinstance(command, SlashCommand):
            context.arguments = {
                option.name: resolve_interaction_option(interaction, option) for option in interaction.options
            }
            return await command._callback(context, **context.arguments)  # type: ignore

        if isinstance(command, SlashCommandGroup):
            callback: CommandCallbackT | None = None
            sub_command_group, sub_command = None, None
            sub_commands: dict[str, SubCommandMethod] = command.get_sub_commands()
            options: list[CommandInteractionOption] = list(interaction.options)
            while options:
                option = options.pop()
                if option.type == OptionType.SUB_COMMAND_GROUP:
                    sub_command_group = command.sub_commands.get(option.name)
                    if not sub_command_group:
                        raise SubCommandNotFound(command.name, option.name)
                    options = list(option.options or [])
                    sub_commands = sub_command_group.command.sub_commands or {}
                elif option.type == OptionType.SUB_COMMAND:
                    sub_command = sub_commands.get(option.name)
                    if not sub_command:
                        if sub_command_group:
                            raise SubCommandNotFound(command.name, sub_command_group.command.name, option.name)
                        raise SubCommandNotFound(command.name, option.name)
                    options = list(option.options or [])
                    callback = sub_command.method(command)
                else:
                    context.arguments[option.name] = resolve_interaction_option(interaction, option)
            assert callback
            await callback(context, **context.arguments)

        if isinstance(command, UserCommand):
            if not hasattr(command, "callback"):
                raise CommandCallbackNotImplemented(command.name)
            return await command.callback(context, *interaction.resolved.users.values())  # type: ignore

        if isinstance(command, MessageCommand):
            if not hasattr(command, "callback"):
                raise CommandCallbackNotImplemented(command.name)
            return await command.callback(context, *interaction.resolved.messages.values())  # type: ignore

    async def on_command_interaction(self, event: InteractionCreateEvent) -> None:
        """Handle command interaction events.

        This method processes incoming interaction event and executes the appropriate command.

        Parameters
        ----------
        event : InteractionCreateEvent
            The interaction event to handle.

        Raises
        ------
        SubCommandNotFound
            If a specified sub-command or sub-command group is not found.
        CommandCallbackNotImplemented
            If a required callback method is not implemented for a command.
        CommandNotFound
            If the command specified in the interaction is not found.
        """
        if isinstance(event.interaction, CommandInteraction):
            command: BaseCommand | None = None
            if command_guild_id := event.interaction.registered_guild_id:
                if event.interaction.guild_id != command_guild_id:
                    return
                command = self.guild_commands.get(command_guild_id, {}).get(event.interaction.command_id)
            else:
                command = self.global_commands.get(event.interaction.command_id)

            if not command:
                raise CommandNotFound(event.interaction.command_name)

            async with timeit(trace, f"completed {event.interaction.command_name} in %.6f seconds"):
                await self.execute_command(event.interaction, command)
