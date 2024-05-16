from __future__ import annotations

import typing

from hikari.commands import CommandChoice, CommandOption, CommandType, OptionType
from hikari.permissions import Permissions
from hikari.undefined import UNDEFINED

from aurum.commands.sub_commands import SubCommand
from aurum.internal.commands.app_command import AppCommand
from aurum.internal.consts import SUB_COMMANDS_VAR
from aurum.l10n import Localized

if typing.TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from hikari.api import SlashCommandBuilder
    from hikari.guilds import PartialGuild
    from hikari.snowflakes import SnowflakeishOr
    from hikari.undefined import UndefinedType

    from aurum.l10n import LocalizationProviderInterface, LocalizedOr
    from aurum.options import Option


class SlashCommandMeta(type):
    def __new__(
        mcs: typing.Type[SlashCommandMeta],
        name: str,
        bases: typing.Tuple[type, ...],
        attrs: typing.Dict[str, typing.Any],
    ) -> SlashCommandMeta:
        cls: SlashCommandMeta = super().__new__(mcs, name, bases, attrs)
        setattr(cls, SUB_COMMANDS_VAR, {})
        for name, obj in attrs.items():
            if isinstance(obj, SubCommand):
                getattr(cls, SUB_COMMANDS_VAR)[obj.name] = obj
        return cls


class SlashCommand(AppCommand, metaclass=SlashCommandMeta):
    """
    Represents a slash-command.

    Attributes:
        _app (PartialCommand): Command application instance, available after sync.
        command_type (CommandType): Type of the command.
        name (str): The command name.
        description (LocalizedOr[str] | None): Optional description of the command for help documentation.
        guild (SnowflakeishOr[PartialGuild] | UndefinedType): Optional guild (server) where the command is available.
        default_member_permissions (Permissions): The permissions a user must have to use the command by default.
        dm_enabled (bool): Whether the command can be used in direct messages.
        is_nsfw (bool): Indicates whether the command is age-restricted.
        options (Sequence[Option]): Options to the command.
        sub_commands (Dict[str, SubCommand]): Sub-commands of the command.

    Args:
        name (str): The unique name of the command.
        description (LocalizedOr[str] | None): A description of command.
        guild (SnowflakeishOr[PartialGuild] | UndefinedType): The guild in which the command is available.
        default_member_permissions (Permissions): Permissions required to use the command, if any. Defaults to NONE.
        dm_enabled (bool): Flag indicating whether the command is available in direct messages. Defaults to `False`.
        is_nsfw (bool): Flag indicating whether the command should only be available in NSFW channels. Defaults to `False`.
        options (Sequence[Option]): Options to the command.

    Methods:
        Inherited from AppCommand class.

    Note:
        If your command has sub-commands, the callback will not be executed.

    Example:
        ```py
        class HelloCommand(SlashCommand):
            def __init__(self) -> None:
                super().__init__(name="hello", description="Say hi to bot")

            async def callback(self, context: InteractionContext) -> None:
                await context.create_response(f"Hi, {context.user.mention}!")
        ```

    Example with sub-commands:
        ```py
        class ABCCommand(SlashCommand):
            def __init__(self) -> None:
                super().__init__(name="a")

            @sub_command(name="b")
            async def b_command(self, context: InteractionContext) -> None:
                ...

            @b_command.sub_command(name="c")
            async def b_c_command(self, context: InteractionContext) -> None:
                ...
        ```
    """

    __slots__: Sequence[str] = (
        "_app",
        "command_type",
        "name",
        "description",
        "guild",
        "default_member_permissions",
        "dm_enabled",
        "is_nsfw",
        "options",
        "sub_commands",
    )

    def __init__(
        self,
        name: str,
        description: LocalizedOr[str] | None = None,
        *,
        guild: SnowflakeishOr[PartialGuild] | UndefinedType = UNDEFINED,
        default_member_permissions: Permissions = Permissions.NONE,
        dm_enabled: bool = False,
        is_nsfw: bool = False,
        options: Sequence[Option] = (),
    ) -> None:
        super().__init__(
            command_type=CommandType.SLASH,
            name=name,
            description=description,
            guild=guild,
            default_member_permissions=default_member_permissions,
            dm_enabled=dm_enabled,
            is_nsfw=is_nsfw,
        )
        self.options: Sequence[Option] = options
        self.sub_commands: typing.Dict[str, SubCommand] = getattr(self, SUB_COMMANDS_VAR, {})

    def __build_option(self, option: Option, l10n: LocalizationProviderInterface) -> CommandOption:
        choices: tuple[CommandChoice, ...] = tuple(
            CommandChoice(
                name=str(choice.name),
                name_localizations=(
                    l10n.build_localized(choice.name) if isinstance(choice.name, Localized) else {}
                ),
                value=choice.value,
            )
            for choice in option.choices
        )
        return CommandOption(
            type=option.type,
            name=str(option.name),
            name_localizations=(
                l10n.build_localized(option.name) if isinstance(option.name, Localized) else {}
            ),
            description=str(option.description),
            description_localizations=(
                l10n.build_localized(option.description)
                if isinstance(option.description, Localized)
                else {}
            ),
            is_required=option.is_required,
            choices=choices,
            channel_types=getattr(option, "channel_types", None),
            autocomplete=False,  # TODO: autocomplete
            min_value=getattr(option, "min_value", None),
            max_value=getattr(option, "max_value", None),
            min_length=getattr(option, "min_length", None),
            max_length=getattr(option, "max_length", None),
        )

    def __build_sub_group(
        self, command_group: SubCommand, l10n: LocalizationProviderInterface
    ) -> CommandOption:
        return CommandOption(
            type=OptionType.SUB_COMMAND_GROUP,
            name=command_group.name,
            description=command_group.name,
            options=[
                self.__build_sub_command(command, l10n)
                for command in command_group.sub_commands.values()
            ],
        )

    def __build_sub_command(
        self, command: SubCommand, l10n: LocalizationProviderInterface
    ) -> CommandOption:
        return CommandOption(
            type=OptionType.SUB_COMMAND,
            name=command.name,
            description=str(command.description),
            options=[self.__build_option(option, l10n) for option in command.options],
            description_localizations=(
                l10n.build_localized(command.description)
                if isinstance(command.description, Localized)
                else {}
            ),
        )

    def get_builder(
        self,
        factory: Callable[[str, str], SlashCommandBuilder],
        l10n: LocalizationProviderInterface,
    ) -> SlashCommandBuilder:
        description: str = str(self.description) if not self.sub_commands else self.name
        builder: SlashCommandBuilder = (
            factory(self.name, description)
            .set_default_member_permissions(self.default_member_permissions)
            .set_is_dm_enabled(self.dm_enabled)
            .set_is_nsfw(self.is_nsfw)
        )
        if not self.sub_commands:
            if isinstance(self.description, Localized):
                builder.set_description_localizations(l10n.build_localized(self.description))
        for command in self.sub_commands.values():
            if command.sub_commands:
                builder.add_option(self.__build_sub_group(command, l10n))
            else:
                builder.add_option(self.__build_sub_command(command, l10n))
        for option in self.options:
            builder.add_option(self.__build_option(option, l10n))
        return builder
