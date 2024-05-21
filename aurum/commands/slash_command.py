from __future__ import annotations

import typing

from hikari.commands import CommandType
from hikari.permissions import Permissions
from hikari.undefined import UNDEFINED

from aurum.commands.sub_command import SubCommand
from aurum.internal.commands.app_command import AppCommand
from aurum.internal.consts import SUB_COMMANDS_CONTAINER
from aurum.internal.utils.commands import build_option
from aurum.l10n.localized import Localized

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
        setattr(cls, SUB_COMMANDS_CONTAINER, {})
        for name, obj in attrs.items():
            if isinstance(obj, SubCommand):
                getattr(cls, SUB_COMMANDS_CONTAINER)[obj.name] = obj
        return cls


class SlashCommand(AppCommand, metaclass=SlashCommandMeta):
    """Represents a slash-command.

    Args:
        name (str): The unique name of the command.
        description (LocalizedOr[str] | None): A description of command.
        guild (SnowflakeishOr[PartialGuild] | UndefinedType): The guild in which the command is available.
        default_member_permissions (Permissions): Permissions required to use the command, if any. Defaults to NONE.
        is_dm_enabled (bool): Flag indicating whether the command is available in direct messages. Defaults to `False`.
        is_nsfw (bool): Flag indicating whether the command should only be available in NSFW channels. Defaults to `False`.
        options (Sequence[Option]): Options to the command.

    Attributes:
        options (Sequence[Option]): Options to the command.
        sub_commands (Dict[str, SubCommand]): Sub-commands of the command.

    Example:
        === "With callback"
            ```py
            class HelloCommand(SlashCommand):
            def __init__(self) -> None:
                super().__init__(name="hello", description="Say hi to bot")  # (1)

            async def callback(self, context: InteractionContext) -> None:
                await context.create_response(f"Hi, {context.user.mention}!")
            ```

            1. Base information about your command: name, description, default member permissions and etc.

        === "With sub-commands"
            ```py
            class ABCCommand(SlashCommand):  # (1)
            def __init__(self) -> None:
                super().__init__(name="a")  # (2)

            @sub_command(name="b")  # (3)
            async def b_command(self, context: InteractionContext) -> None:
                ...  # (4)

            @b_command.sub_command(name="c")
            async def b_c_command(self, context: InteractionContext) -> None:
                ...
            ```

            1. When command has a sub-commands, callback will be ignored.
            2. Base information about your command: name, description, default member permissions and etc.
            3. Base information about your sub-command.
                The same fields with slash-command, but without guild, default member permissions, is nsfw, dm enabled flags.
            4. If sub-command have another sub-command, callback of parent sub-command will be ignored too.
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
        is_dm_enabled: bool = False,
        is_nsfw: bool = False,
        options: Sequence[Option] = (),
    ) -> None:
        super().__init__(
            command_type=CommandType.SLASH,
            name=name,
            description=description,
            guild=guild,
            default_member_permissions=default_member_permissions,
            is_dm_enabled=is_dm_enabled,
            is_nsfw=is_nsfw,
        )
        self.options: Sequence[Option] = options
        self.sub_commands: typing.Dict[str, SubCommand] = getattr(self, SUB_COMMANDS_CONTAINER, {})

    def get_builder(
        self,
        factory: Callable[[str, str], SlashCommandBuilder],
        l10n: LocalizationProviderInterface,
    ) -> SlashCommandBuilder:
        description: LocalizedOr[str] = self.description or "No description"
        builder: SlashCommandBuilder = (
            factory(self.name, str(description))
            .set_default_member_permissions(self.default_member_permissions)
            .set_is_dm_enabled(self.is_dm_enabled)
            .set_is_nsfw(self.is_nsfw)
        )
        if not self.sub_commands:
            if isinstance(description, Localized):
                builder.set_description_localizations(l10n.build_localized(description))
            for option in self.options:
                builder.add_option(build_option(option, l10n))
        else:
            for sub_command in self.sub_commands.values():
                builder.add_option(sub_command.as_option(l10n))
        return builder
