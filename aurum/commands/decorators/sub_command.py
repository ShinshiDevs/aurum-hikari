from __future__ import annotations

from collections.abc import Callable, Sequence

from aurum.commands.sub_command import SubCommand
from aurum.commands.typing import CommandCallbackT
from aurum.hooks import Hook
from aurum.l10n import LocalizedOr
from aurum.option import Option


def sub_command(
    name: str | None = None,
    description: LocalizedOr[str] = "No description",
    *,
    display_name: LocalizedOr[str] | None = None,
    options: Sequence[Option] = (),
    hooks: Sequence[Hook] = (),
) -> Callable[[CommandCallbackT], SubCommand]:
    """Decorator for the sub-command.

    Can be used only in a command class that inherits from `aurum.commands.slash_command.SlashCommand`.

    Args:
        name (str): The unique name for the sub-command.
        description (LocalizedOr[str] | None): Optional description for the sub-command.
        display_name (LocalizedOr[str] | None): A display name of command.
            Can be localized.
        options (Sequence[Option]): Optional options of the sub-command.

    Note:
        The callback must be asynchronous.
    """

    def decorator(func: CommandCallbackT) -> SubCommand:
        return SubCommand(
            callback=func,
            name=name or func.__name__,
            description=description,
            display_name=display_name,
            options=options,
            hooks=hooks,
        )

    return decorator
