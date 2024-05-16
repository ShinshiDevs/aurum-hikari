from __future__ import annotations

import typing

from aurum.commands.sub_commands import SubCommand

if typing.TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Sequence

    from aurum.l10n import LocalizedOr
    from aurum.options import Option


def sub_command(
    name: str,
    description: LocalizedOr[str] | None = None,
    options: Sequence[Option] = (),
) -> Callable[..., SubCommand]:
    def decorator(func: Callable[..., Awaitable[None]]) -> SubCommand:
        return SubCommand(
            callback=func,
            name=name,
            description=description,
            options=options,
        )

    return decorator
