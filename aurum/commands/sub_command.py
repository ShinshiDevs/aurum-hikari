from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Dict

import attrs

from aurum.commands.typing import CommandCallbackT
from aurum.hook import Hook
from aurum.l10n import LocalizedOr
from aurum.option import Option

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
    hooks: Sequence[Hook] = attrs.field(factory=tuple, repr=False, eq=False)

    sub_commands: Dict[str, SubCommand] = attrs.field(factory=dict, repr=False, eq=False)

    def sub_command(
        self,
        name: str,
        *,
        display_name: LocalizedOr[str] | None = None,
        description: LocalizedOr[str] = "No description",
        options: Sequence[Option] = (),
        hooks: Sequence[Hook] = (),
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
                hooks=hooks,
            )

        return decorator
