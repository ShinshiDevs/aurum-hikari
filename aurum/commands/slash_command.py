from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Dict, Tuple, Type

from hikari.commands import OptionType
from hikari.commands import SlashCommand as HikariSlashCommand
from hikari.interactions import CommandInteraction, CommandInteractionOption
from hikari.permissions import Permissions
from hikari.snowflakes import Snowflakeish
from hikari.undefined import UNDEFINED, UndefinedOr

from aurum.commands.constants import COMMAND_CALLBACK_FLAG, SUB_COMMANDS
from aurum.commands.sub_command import SubCommand
from aurum.hooks import Hook
from aurum.i18n import Translatable
from aurum.interaction import InteractionContext
from aurum.options import Option
from aurum.utils import cast_translatable


class SlashCommandMeta(type):
    def __new__(
        mcs: Type[SlashCommandMeta],
        name: str,
        bases: Tuple[type, ...],
        attrs: Dict[str, Any],
    ) -> SlashCommandMeta:
        cls: SlashCommandMeta = super().__new__(mcs, name, bases, attrs)
        setattr(cls, SUB_COMMANDS, {})
        for name, obj in attrs.items():
            if getattr(obj, COMMAND_CALLBACK_FLAG, False):
                setattr(cls, SUB_COMMANDS, {})
                setattr(cls, COMMAND_CALLBACK_FLAG, obj)
                break
            else:
                if isinstance(obj, SubCommand):
                    getattr(cls, SUB_COMMANDS)[obj.name] = obj
        return cls


class SlashCommand(metaclass=SlashCommandMeta):
    __slots__: Sequence[str] = (
        COMMAND_CALLBACK_FLAG,
        SUB_COMMANDS,
        "name",
        "description",
        "options",
        "guild",
        "default_member_permissions",
        "is_dm_enabled",
        "is_nsfw",
        "hooks",
        "after_hooks",
    )

    def __init__(
        self,
        name: str,
        description: str | Translatable = "No description",
        *,
        options: Sequence[Option] = (),
        guild: UndefinedOr[Snowflakeish] = UNDEFINED,
        default_member_permissions: Permissions = Permissions.NONE,
        is_dm_enabled: bool = False,
        is_nsfw: bool = False,
        hooks: Sequence[Hook] = (),
        after_hooks: Sequence[Hook] = (),
    ) -> None:
        self._app: HikariSlashCommand | None = None

        self.name: str = name
        self.description: Translatable = cast_translatable(description)

        self.guild: UndefinedOr[Snowflakeish] = guild

        self.default_member_permissions: Permissions = default_member_permissions
        self.is_dm_enabled: bool = is_dm_enabled
        self.is_nsfw: bool = is_nsfw

        self.hooks: Sequence[Hook] = hooks
        self.after_hooks: Sequence[Hook] = after_hooks

        if getattr(self, COMMAND_CALLBACK_FLAG, None):
            self.options: Sequence[Option] = options

    @property
    def app(self) -> HikariSlashCommand | None:
        return self._app

    @app.setter
    def app(self, value: HikariSlashCommand) -> None:
        self._app = value

    async def execute(self, context: InteractionContext) -> Any:
        if not isinstance(context.interaction, CommandInteraction):
            raise TypeError(
                f"Invalid interaction for slash command execution: {type(context.interaction)}"
            )
        group_name: str | None = None
        options: Sequence[CommandInteractionOption] = context.interaction.options or ()
        arguments: Dict[str, Any] = {}
        if callback := getattr(self, COMMAND_CALLBACK_FLAG, None):
            for option in options:
                arguments[option.name] = context.resolve_command_option(option)
            return await callback(self, context, **arguments)
        for option in options:
            if option.type is OptionType.SUB_COMMAND_GROUP:
                group_name = option.name
                options = option.options or ()
        for option in options:
            if option.type is OptionType.SUB_COMMAND:
                options = option.options or ()
                group = getattr(self, SUB_COMMANDS).get(group_name)
                sub_command = group.commands.get(
                    option.name, getattr(self, SUB_COMMANDS).get(option.value)
                )
        for option in options:
            arguments[option.name] = context.resolve_command_option(option)
        if callback := getattr(sub_command, "callback", None):
            await callback(self, context, **arguments)
