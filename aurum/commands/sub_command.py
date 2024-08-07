from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Dict

import attrs
from hikari.commands import CommandOption, OptionType

from aurum.commands.typing import CommandCallbackT
from aurum.internal.utils.commands import build_option
from aurum.l10n import LocalizationProviderInterface, Localized, LocalizedOr
from aurum.options import Option

if TYPE_CHECKING:
    from aurum.commands.slash_command import SlashCommand


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class SubCommand:
    parent: SlashCommand | SubCommand | None = attrs.field(default=None, eq=None, repr=False)
    callback: CommandCallbackT = attrs.field()

    name: str
    display_name: LocalizedOr[str] | None = attrs.field(default=None, repr=False, eq=False)
    description: LocalizedOr[str] = attrs.field(default="No description", repr=False, eq=False)

    options: Sequence[Option] = attrs.field(factory=tuple, repr=False, eq=False)
    sub_commands: Dict[str, SubCommand] = attrs.field(factory=dict, repr=False, eq=False)

    def sub_command(
        self,
        name: str,
        *,
        display_name: LocalizedOr[str] | None = None,
        description: LocalizedOr[str] = "No description",
        options: Sequence[Option] = (),
    ) -> Callable[..., None]:
        """Decorator for the sub-command.

        This object can only be created by using the decorator [@sub_command][aurum.commands.decorators.sub_command.sub_command]
        on a function in a class that inherits from [SlashCommand][aurum.commands.slash_command.SlashCommand].

        Args:
            name (str): The unique name for the sub-command.
            description (LocalizedOr[str] | None): Optional description for the sub-command.
            display_name (LocalizedOr[str] | None): A display name of command.
                Can be localized.
            options (Sequence[Option]): Optional options of the sub-command.

        Note:
            The callback must be asynchronous.
        """

        def decorator(func: CommandCallbackT) -> None:
            self.sub_commands[name] = SubCommand(
                parent=self,
                callback=func,
                name=name,
                description=description,
                display_name=display_name,
                options=options,
            )

        return decorator

    def as_option(self, l10n: LocalizationProviderInterface | None) -> CommandOption:
        if l10n and isinstance(self.display_name, Localized):
            l10n.build_localized(self.display_name)
        if l10n and isinstance(self.description, Localized):
            l10n.build_localized(self.description)
        return CommandOption(
            type=OptionType.SUB_COMMAND if not self.sub_commands else OptionType.SUB_COMMAND_GROUP,
            name=self.name,
            name_localizations=(
                localizations
                if isinstance(localizations := getattr(self.display_name, "value", {}), dict)
                else {}
            ),
            description=str(self.description),
            description_localizations=(
                localizations
                if isinstance(localizations := getattr(self.description, "value", {}), dict)
                else {}
            ),
            options=(
                [build_option(option, l10n) for option in self.options]
                if not self.sub_commands
                else [sub_command.as_option(l10n) for sub_command in self.sub_commands.values()]
            ),
        )
