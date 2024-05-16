from __future__ import annotations

import typing

from hikari.commands import CommandType, OptionType
from hikari.events import InteractionCreateEvent
from hikari.interactions import CommandInteraction
from hikari.snowflakes import Snowflake

from aurum.commands.message_command import MessageCommand
from aurum.commands.slash_command import SlashCommand
from aurum.commands.user_command import UserCommand
from aurum.interactions.interaction_context import InteractionContext
from aurum.internal.exceptions.commands_exceptions import UnknownCommandException

if typing.TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from hikari.impl import GatewayBot
    from hikari.interactions import (
        CommandInteractionOption,
        ComponentInteraction,
        PartialInteraction,
    )

    from aurum.client import Client
    from aurum.commands.sub_commands import SubCommand
    from aurum.internal.commands.app_command import AppCommand
    from aurum.internal.commands.command_handler import CommandHandler
    from aurum.l10n import Locale, LocalizationProviderInterface

type ComponentHandler = None  # TODO: Remove that, when ComponentHandler will appear


class InteractionProcessor:
    __slots__: Sequence[str] = (
        "bot",
        "client",
        "l10n",
        "commands",
        "components",
        "ignore_unknown_interactions",
        "get_locale_func",
    )

    def __init__(
        self,
        bot: GatewayBot,
        client: Client,
        l10n: LocalizationProviderInterface,
        commands: CommandHandler,
        components: ComponentHandler,
        ignore_unknown_interactions: bool,
        get_locale_func: Callable[[CommandInteraction | ComponentInteraction], Locale],
    ) -> None:
        self.bot: GatewayBot = bot
        self.client: Client = client
        self.l10n: LocalizationProviderInterface = l10n

        self.commands: CommandHandler = commands
        self.components: ComponentHandler = components

        self.ignore_unknown_interactions: bool = ignore_unknown_interactions

        self.get_locale_func: Callable[[CommandInteraction | ComponentInteraction], Locale] = (
            get_locale_func
        )

    def create_interaction_context(
        self, interaction: ComponentInteraction | CommandInteraction
    ) -> InteractionContext:
        return InteractionContext(
            interaction=interaction,
            bot=self.bot,
            client=self.client,
            locale=self.get_locale_func(interaction),
        )

    async def on_interaction(self, event: InteractionCreateEvent) -> None:
        interaction: PartialInteraction = event.interaction
        if isinstance(interaction, CommandInteraction):
            return await self.proceed_command(interaction)

    async def proceed_command(self, interaction: CommandInteraction) -> None:
        context: InteractionContext = self.create_interaction_context(interaction)
        parent_command: AppCommand | None = self.commands.commands.get(interaction.command_name)
        if not parent_command:
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
                    if not command:
                        raise UnknownCommandException(option.name, interaction.command_name)
                elif option.type is OptionType.SUB_COMMAND_GROUP:
                    sub_command_group: SubCommand | None = command.sub_commands.get(option.name)
                    if not sub_command_group:
                        raise UnknownCommandException(option.name, interaction.command_name)
                    if options := option.options:
                        command = sub_command_group.sub_commands.get(options[0].name)
                        options = options[0].options
                        if not command:
                            raise UnknownCommandException(
                                option.name, sub_command_group.name, interaction.command_name
                            )
                for option in options or ():
                    arguments[option.name] = self.resolve_command_argument(interaction, option)
            return await (
                command.callback(context, **arguments)
                if isinstance(command, SlashCommand)
                else command.callback(parent_command, context, **arguments)
            )
        if interaction.command_type is CommandType.MESSAGE:
            assert isinstance(command, MessageCommand)
            assert interaction.resolved
            return await command.callback(
                context,
                list(interaction.resolved.messages.values())[0],
            )
        if interaction.command_type is CommandType.USER:
            assert isinstance(command, UserCommand)
            assert interaction.resolved
            return await command.callback(
                context,
                list(interaction.resolved.users.values())[0],
            )

    def resolve_command_argument(
        self, interaction: CommandInteraction, option: CommandInteractionOption
    ) -> typing.Any:
        if not interaction.resolved or not isinstance(option.value, Snowflake):
            return option.value
        match option.type:
            case OptionType.USER:
                return interaction.resolved.members.get(
                    option.value,
                    interaction.resolved.users.get(option.value),
                )
            case OptionType.CHANNEL:
                return interaction.resolved.channels.get(option.value)
            case OptionType.ROLE:
                return interaction.resolved.roles.get(option.value)
            case OptionType.MENTIONABLE:
                return interaction.resolved.members.get(
                    option.value,
                    interaction.resolved.roles.get(option.value),
                )
            case OptionType.ATTACHMENT:
                return interaction.resolved.attachments.get(option.value)
