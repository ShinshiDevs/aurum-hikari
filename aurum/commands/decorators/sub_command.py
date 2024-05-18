from __future__ import annotations

import typing

from aurum.commands.sub_command import SubCommand

if typing.TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Sequence

    from aurum.l10n import LocalizedOr
    from aurum.options import Option


def sub_command(
    name: str,
    description: LocalizedOr[str] | None = None,
    options: Sequence[Option] = (),
) -> Callable[..., SubCommand]:
    """Decorator for the sub-command.

    Can be used only in a command class that inherits from `aurum.commands.slash_command.SlashCommand`.

    Args:
        name (str): The unique name for the sub-command.
        description (LocalizedOr[str] | None): Optional description for the sub-command.
        options (Sequence[Option]): Optional options of the sub-command.

    Note:
        The callback must be asynchronous.
    """

    def decorator(func: Callable[..., Awaitable[None]]) -> SubCommand:
        return SubCommand(
            callback=func,
            name=name,
            description=description,
            options=options,
        )

    return decorator
