from __future__ import annotations

import typing

from hikari.commands import CommandType, OptionType
from hikari.events import InteractionCreateEvent
from hikari.interactions import CommandInteraction
from hikari.snowflakes import Snowflake

from aurum.commands.message_command import MessageCommand
from aurum.commands.slash_command import SlashCommand
from aurum.commands.user_command import UserCommand
from aurum.exceptions.commands_exceptions import UnknownCommandException
from aurum.interactions.interaction_context import InteractionContext

if typing.TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from hikari.impl import GatewayBot
    from hikari.interactions import (
        CommandInteractionOption,
        ComponentInteraction,
        PartialInteraction,
    )

    from aurum.client import Client
    from aurum.commands.app_command import AppCommand
    from aurum.commands.command_handler import CommandHandler
    from aurum.commands.sub_commands import SubCommand
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
        command: AppCommand | None = self.commands.commands.get(interaction.command_name)
        if not command and not self.ignore_unknown_interactions:
            raise UnknownCommandException(interaction.command_name)
        if interaction.command_type is CommandType.SLASH:
            assert isinstance(command, SlashCommand)
            arguments: typing.Dict[str, typing.Any] = {}
            if options := interaction.options:
                if options[0].type is OptionType.SUB_COMMAND_GROUP:
                    return await self.proceed_sub_command_group(context, interaction, command)
                elif options[0].type is OptionType.SUB_COMMAND:
                    return await self.proceed_sub_command(context, interaction, command, options)
                else:
                    for option in options:
                        arguments[option.name] = self.resolve_command_argument(interaction, option)
            return await command.callback(context, **arguments)
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

    async def proceed_sub_command(
        self,
        context: InteractionContext,
        interaction: CommandInteraction,
        command: SlashCommand | SubCommand,
        options: Sequence[CommandInteractionOption],
    ) -> None:
        arguments: typing.Dict[str, typing.Any] = {}
        sub_command: SubCommand | None = command.sub_commands.get(options[0].name)
        if not sub_command and not self.ignore_unknown_interactions:
            raise UnknownCommandException(interaction.options[0].name, interaction.command_name)
        if options := interaction.options[0].options:
            for option in options:
                arguments[option.name] = self.resolve_command_argument(interaction, option)
        await sub_command.callback(context, **arguments)

    async def proceed_sub_command_group(
        self, context: InteractionContext, interaction: CommandInteraction, command: SlashCommand
    ) -> None:
        sub_command_group: SubCommand | None = command.sub_commands.get(interaction.options[0].name)
        if not sub_command_group and not self.ignore_unknown_interactions:
            raise UnknownCommandException(interaction.options[0].name, interaction.command_name)
        if options := interaction.options[0].options:
            return await self.proceed_sub_command(context, interaction, sub_command_group, options)

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
