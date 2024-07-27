from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Dict, Tuple, Type

from hikari.commands import CommandType
from hikari.guilds import PartialGuild
from hikari.permissions import Permissions
from hikari.snowflakes import SnowflakeishOr
from hikari.undefined import UNDEFINED, UndefinedType

from aurum.commands.app_command import AppCommand
from aurum.commands.sub_command import SubCommand
from aurum.commands.typing import AutocompletesDictT, SubCommandsDictT
from aurum.hooks import Hook
from aurum.l10n import LocalizedOr
from aurum.option import Option


class SlashCommandMeta(type):
    def __new__(
        mcs: Type[SlashCommandMeta], name: str, bases: Tuple[type, ...], attrs: Dict[str, Any]
    ) -> SlashCommandMeta:
        attrs["sub_commands"] = {
            obj.name: obj for obj in attrs.values() if isinstance(obj, SubCommand)
        }
        return super().__new__(mcs, name, bases, attrs)


class SlashCommand(AppCommand, metaclass=SlashCommandMeta):
    """Represents a slash-command.

    Args:
        name (str): The unique name of the command.
        description (LocalizedOr[str] | None): A description of command.
        display_name (LocalizedOr[str] | None): A display name of command.
            Can be localized.
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

    command_type: CommandType = CommandType.SLASH

    __slots__: Sequence[str] = (
        "name",
        "display_name",
        "description",
        "dm_enabled",
        "options",
        "hooks",
        "autocompletes",
    )

    def __init__(
        self,
        name: str,
        *,
        display_name: LocalizedOr[str] | None = None,
        description: LocalizedOr[str] = "No description",
        guild: SnowflakeishOr[PartialGuild] | UndefinedType = UNDEFINED,
        default_member_permissions: Permissions = Permissions.NONE,
        is_dm_enabled: bool = False,
        is_nsfw: bool = False,
        options: Sequence[Option] = (),
        hooks: Sequence[Hook] = (),
    ) -> None:
        super().__init__(
            name=name,
            display_name=display_name,
            guild=guild,
            default_member_permissions=default_member_permissions,
            is_dm_enabled=is_dm_enabled,
            is_nsfw=is_nsfw,
        )
        self.description: LocalizedOr[str] = description
        self.options: Sequence[Option] = options
        self.hooks: Sequence[Hook] = hooks
        self.sub_commands: SubCommandsDictT = getattr(self, "sub_commands", {})  # type: ignore
        self.autocompletes: AutocompletesDictT = {}
