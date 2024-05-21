from __future__ import annotations

import typing
from dataclasses import dataclass, field

from hikari.commands import CommandOption, OptionType

from aurum.internal.utils.commands import build_option
from aurum.l10n.localized import Localized
from aurum.options import Option

if typing.TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Sequence

    from aurum.l10n import LocalizationProviderInterface
    from aurum.l10n.types import LocalizedOr


@dataclass(slots=True, kw_only=True)
class SubCommand:
    callback: Callable[..., Awaitable[typing.Any]]

    name: str
    description: LocalizedOr[str] | None = None

    options: Sequence[Option] = field(default_factory=tuple[Option])

    sub_commands: typing.Dict[str, SubCommand] = field(default_factory=dict)

    def sub_command(
        self,
        name: str,
        description: LocalizedOr[str] | None = None,
        options: Sequence[Option] = (),
    ) -> Callable[..., None]:
        """Decorator for the sub-command.

        This object can only be created by using the decorator [@sub_command][aurum.commands.decorators.sub_command.sub_command]
        on a function in a class that inherits from [SlashCommand][aurum.commands.slash_command.SlashCommand].

        Args:
            name (str): The unique name for the sub-command.
            description (LocalizedOr[str] | None): Optional description for the sub-command.
            options (Sequence[Option]): Optional options of the sub-command.

        Note:
            The callback must be asynchronous.
        """

        def decorator(func: Callable[..., Awaitable[None]]) -> None:
            self.sub_commands[name] = SubCommand(
                callback=func,
                name=name,
                description=description or "No description",
                options=options,
            )

        return decorator

    def as_option(self, l10n: LocalizationProviderInterface) -> CommandOption:
        options: Sequence[CommandOption]
        if not self.sub_commands:
            options = [build_option(option, l10n) for option in self.options]
        else:
            options = [sub_command.as_option(l10n) for sub_command in self.sub_commands.values()]
        description: LocalizedOr[str] = self.description or "No description"
        return CommandOption(
            type=OptionType.SUB_COMMAND if not self.sub_commands else OptionType.SUB_COMMAND_GROUP,
            name=str(self.name),  # TODO: display name
            description=str(description),
            description_localizations=(
                l10n.build_localized(description) if isinstance(description, Localized) else {}
            ),
            options=options,
        )
