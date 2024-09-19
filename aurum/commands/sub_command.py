from __future__ import annotations

from collections.abc import Callable, Sequence

import attrs

from aurum.commands.typing import AutocompletesDictT, CommandCallbackT, SubCommandsDictT
from aurum.hooks import Hook
from aurum.l10n import LocalizedOr
from aurum.option import Option


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class SubCommand:
    callback: CommandCallbackT = attrs.field()

    name: str = attrs.field()
    description: LocalizedOr[str] = attrs.field(default="No description", repr=False, eq=False)
    display_name: LocalizedOr[str] | None = attrs.field(default=None, repr=False, eq=False)

    options: Sequence[Option] = attrs.field(factory=tuple, repr=False, eq=False)
    hooks: Sequence[Hook] = attrs.field(factory=tuple, repr=False, eq=False)

    sub_commands: SubCommandsDictT = attrs.field(factory=dict, repr=False, eq=False)
    autocompletes: AutocompletesDictT = attrs.field(factory=dict, repr=False, eq=False)

    def sub_command(
        self,
        name: str | None = None,
        description: LocalizedOr[str] = "No description",
        *,
        display_name: LocalizedOr[str] | None = None,
        options: Sequence[Option] = (),
        hooks: Sequence[Hook] = (),
    ) -> Callable[[CommandCallbackT], None]:
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
            self.sub_commands[name or func.__name__] = SubCommand(
                callback=func,
                name=name or func.__name__,
                description=description,
                display_name=display_name,
                options=options,
                hooks=hooks,
            )

        return decorator
