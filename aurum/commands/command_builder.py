from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from hikari.api import ContextMenuCommandBuilder, SlashCommandBuilder
from hikari.commands import CommandChoice, CommandOption, OptionType
from hikari.traits import GatewayBotAware

from aurum.commands.context_menu_command import ContextMenuCommand
from aurum.commands.slash_command import SlashCommand
from aurum.commands.sub_command import SubCommand
from aurum.l10n import LocalizationProviderInterface, Localized
from aurum.option import Choice, Option

if TYPE_CHECKING:
    from aurum.commands.command_handler import CommandHandler


class CommandBuilder:
    __slots__: Sequence[str] = ("bot", "commands", "l10n")

    def __init__(
        self,
        bot: GatewayBotAware,
        commands: CommandHandler,
        l10n: LocalizationProviderInterface | None,
    ) -> None:
        self.bot: GatewayBotAware = bot
        self.commands: CommandHandler = commands
        self.l10n: LocalizationProviderInterface | None = l10n

    def get_localizations(self, localized: Localized | Any) -> dict[str, str]:
        return (
            localized.value
            if isinstance(localized, Localized) and isinstance(localized.value, dict)
            else {}
        )

    def get_choice(self, choice: Choice) -> CommandChoice:
        if self.l10n and isinstance(choice.name, Localized):
            self.l10n.build_localized(choice.name)
        return CommandChoice(
            name=str(choice.name),
            name_localizations=self.get_localizations(choice.name),
            value=choice.value,
        )

    def get_option(self, option: Option, command: SlashCommand | SubCommand) -> CommandOption:
        if self.l10n and isinstance(option.description, Localized):
            self.l10n.build_localized(option.description)
        if self.l10n and isinstance(option.display_name, Localized):
            self.l10n.build_localized(option.display_name)
        if option.autocomplete:
            command.autocompletes[option.name] = option
        return CommandOption(
            type=option.type,
            name=option.name,
            name_localizations=self.get_localizations(option.display_name),
            description=str(option.description),
            description_localizations=self.get_localizations(option.description),
            choices=(
                [self.get_choice(choice) for choice in option.choices]
                if not option.autocomplete
                else []
            ),
            is_required=option.is_required,
            autocomplete=bool(option.autocomplete),
            max_length=option.max_length,
            min_length=option.min_length,
            max_value=option.max_value,
            min_value=option.min_value,
            channel_types=option.channel_types,
        )

    def get_sub_command(self, command: SubCommand) -> CommandOption:
        if self.l10n and isinstance(command.display_name, Localized):
            self.l10n.build_localized(command.display_name)
        if self.l10n and isinstance(command.description, Localized):
            self.l10n.build_localized(command.description)
        if command.sub_commands:
            return CommandOption(
                type=OptionType.SUB_COMMAND_GROUP,
                name=command.name,
                name_localizations=self.get_localizations(command.display_name),
                description="No description",
                options=[
                    self.get_sub_command(sub_command)
                    for sub_command in command.sub_commands.values()
                ],
            )
        return CommandOption(
            type=OptionType.SUB_COMMAND,
            name=command.name,
            name_localizations=self.get_localizations(command.display_name),
            description=str(command.description),
            description_localizations=self.get_localizations(command.description),
            options=[self.get_option(option, command) for option in command.options],
        )

    def get_slash_command(self, command: SlashCommand) -> SlashCommandBuilder:
        if self.l10n and isinstance(command.description, Localized):
            self.l10n.build_localized(command.description)
        builder: SlashCommandBuilder = (
            self.bot.rest.slash_command_builder(command.name, str(command.description))
            .set_default_member_permissions(command.default_member_permissions)
            .set_is_dm_enabled(command.is_dm_enabled)
            .set_is_nsfw(command.is_nsfw)
        )
        if not command.sub_commands:
            if self.l10n and isinstance(command._display_name, Localized):
                self.l10n.build_localized(command._display_name)
                builder.set_name_localizations(self.get_localizations(command._display_name))
            builder.set_description_localizations(self.get_localizations(command.description))
            for option in command.options:
                builder.add_option(self.get_option(option, command))
        else:
            for sub_command in command.sub_commands.values():
                builder.add_option(self.get_sub_command(sub_command))
        return builder

    def get_context_menu_command(self, command: ContextMenuCommand) -> ContextMenuCommandBuilder:
        if self.l10n and isinstance(command.display_name, Localized):
            self.l10n.build_localized(command.display_name)
        builder: ContextMenuCommandBuilder = (
            self.bot.rest.context_menu_command_builder(command.command_type, command.name)
            .set_name_localizations(self.get_localizations(command.display_name))
            .set_default_member_permissions(command.default_member_permissions)
            .set_is_dm_enabled(command.is_dm_enabled)
            .set_is_nsfw(command.is_nsfw)
        )
        return builder
