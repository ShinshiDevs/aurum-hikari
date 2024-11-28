from collections.abc import Callable, Sequence

from hikari.api import special_endpoints as api
from hikari.commands import CommandChoice, CommandOption, CommandType, OptionType
from hikari.permissions import Permissions
from hikari.traits import RESTAware

from aurum.commands.base_command import BaseCommand
from aurum.commands.context_menu_command import ContextMenuCommand, MessageCommand, UserCommand
from aurum.commands.options import Choice, Option
from aurum.commands.slash_command import SlashCommand, SlashCommandGroup
from aurum.commands.sub_command import SubCommand

__all__: Sequence[str] = ("CommandBuilder",)


class CommandBuilder:
    """A class for building Discord application commands."""

    __slots__: Sequence[str] = ()

    def build_commands(self, bot: RESTAware, commands: dict[str, BaseCommand]) -> dict[BaseCommand, api.CommandBuilder]:
        """Build command builders from command definitions.

        Parameters
        ----------
        bot : RESTAware
            The bot instance that provides REST functionality.
        commands : Dict[str, BaseCommand]
            Dictionary mapping command names to command objects.

        Returns
        -------
        Dict[BaseCommand, api.CommandBuilder]
            Dictionary mapping command objects to their corresponding builders.
        """
        builders: dict[BaseCommand, api.CommandBuilder] = {}
        for command in commands.values():
            if isinstance(command, SlashCommand):
                builders[command] = self._build_slash_command(bot.rest.slash_command_builder, command)
            if isinstance(command, SlashCommandGroup):
                builders[command] = self._build_slash_command_group(bot.rest.slash_command_builder, command)
            if isinstance(command, UserCommand | MessageCommand):
                builders[command] = self._build_context_menu_command(bot.rest.context_menu_command_builder, command)
        return builders

    def _build_slash_command(
        self, factory: Callable[[str, str], api.SlashCommandBuilder], command: SlashCommand
    ) -> api.SlashCommandBuilder:
        """Build a slash command builder from a SlashCommand instance.

        Parameters
        ----------
        factory : Callable[[str, str], api.SlashCommandBuilder]
            Factory function to create the slash command builder.
        command : SlashCommand
            The slash command to build.

        Returns
        -------
        api.SlashCommandBuilder
            The configured slash command builder.
        """
        assert isinstance(command.description, str)
        builder: api.SlashCommandBuilder = (
            factory(command.name, command.description or "No description")
            .set_default_member_permissions(command.default_member_permissions or Permissions.NONE)
            .set_is_dm_enabled(command.is_dm_enabled)
            .set_is_nsfw(command.is_nsfw)
        )
        for option in command.options or ():
            builder.add_option(self._build_option(option))
        if command.name_localizations:
            builder.set_name_localizations(command.name_localizations)
        if command.description_localizations:
            builder.set_description_localizations(command.description_localizations)
        return builder

    def _build_slash_command_group(
        self, factory: Callable[[str, str], api.SlashCommandBuilder], group: SlashCommandGroup
    ) -> api.SlashCommandBuilder:
        """Build a slash command group builder from a SlashCommandGroup instance.

        Parameters
        ----------
        factory : Callable[[str, str], api.SlashCommandBuilder]
            Factory function to create the slash command builder.
        group : SlashCommandGroup
            The command group to build.

        Returns
        -------
        api.SlashCommandBuilder
            The configured slash command group builder.
        """
        builder: api.SlashCommandBuilder = (
            factory(group.name, "No description")
            .set_default_member_permissions(group.default_member_permissions or Permissions.NONE)
            .set_is_dm_enabled(group.is_dm_enabled)
            .set_is_nsfw(group.is_nsfw)
        )
        for wrapper in group.get_sub_commands().values() or ():
            if wrapper.command.sub_command_group:
                break
            builder.add_option(self._build_sub_command(wrapper.command))
        if group.name_localizations:
            builder.set_name_localizations(group.name_localizations)
        return builder

    def _build_sub_command(self, command: SubCommand) -> CommandOption:
        """Build a sub-command option from a SubCommand instance.

        Parameters
        ----------
        command : SubCommand
            The sub-command to build.

        Returns
        -------
        CommandOption
            The configured sub-command option.
        """
        if command.sub_commands:
            return CommandOption(
                type=OptionType.SUB_COMMAND_GROUP,
                name=command.name,
                name_localizations=command.name_localizations or {},
                description="No description",
                description_localizations={},
                options=[self._build_sub_command(wrapper.command) for wrapper in command.sub_commands.values()],
            )
        builder: CommandOption = CommandOption(
            type=OptionType.SUB_COMMAND,
            name=command.name,
            name_localizations=command.name_localizations or {},
            description=command.description or "No description",
            description_localizations=command.description_localizations or {},
            options=[self._build_option(option) for option in (command.options or ())],
        )
        return builder

    def _build_choice(self, choice: Choice) -> CommandChoice:
        """Build a command choice from a Choice instance.

        Parameters
        ----------
        choice : Choice
            The choice to build.

        Returns
        -------
        CommandChoice
            The configured command choice.
        """
        return CommandChoice(name=choice.name, value=choice.value, name_localizations=choice.name_localizations or {})

    def _build_option(self, option: Option) -> CommandOption:
        """Build a command option from an Option instance.

        Parameters
        ----------
        option : Option
            The option to build.

        Returns
        -------
        CommandOption
            The configured command option.
        """
        command_option: CommandOption = CommandOption(
            type=option.type,
            name=option.name,
            name_localizations=option.name_localizations or {},
            description=option.description or "No description",
            description_localizations=option.description_localizations or {},
            choices=tuple(self._build_choice(choice) for choice in option.choices),
            is_required=option.is_required,
            max_length=option.max_length,
            min_length=option.min_length,
            max_value=option.max_value,
            min_value=option.min_value,
            channel_types=option.channel_types,
        )
        return command_option

    def _build_context_menu_command(
        self, factory: Callable[[CommandType, str], api.ContextMenuCommandBuilder], command: ContextMenuCommand
    ) -> api.ContextMenuCommandBuilder:
        """Build a context menu command builder from a ContextMenuCommand instance.

        Parameters
        ----------
        factory : Callable[[CommandType, str], api.ContextMenuCommandBuilder]
            Factory function to create the context menu command builder.
        command : ContextMenuCommand
            The context menu command to build.

        Returns
        -------
        api.ContextMenuCommandBuilder
            The configured context menu command builder.
        """
        builder: api.ContextMenuCommandBuilder = (
            factory(command.type, command.name)
            .set_default_member_permissions(command.default_member_permissions or Permissions.NONE)
            .set_is_dm_enabled(command.is_dm_enabled)
            .set_is_nsfw(command.is_nsfw)
        )
        if command.name_localizations:
            builder.set_name_localizations(command.name_localizations)
        return builder
