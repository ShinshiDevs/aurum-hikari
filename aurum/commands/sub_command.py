from __future__ import annotations

import typing
from dataclasses import dataclass, field

from aurum.options import Option

if typing.TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Sequence

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
                description=description,
                options=options,
            )

        return decorator
