from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING

from aurum.commands.options import Option
from aurum.commands.sub_command import SubCommand, SubCommandMethod
from aurum.commands.types import Localized

if TYPE_CHECKING:
    from aurum.commands.types import CommandCallbackT

__all__: Sequence[str] = ("sub_command",)


def sub_command(
    name: str,
    *,
    name_localizations: Localized | None = None,
    description: str | None = None,
    description_localizations: Localized | None = None,
    options: Sequence[Option] | None = None,
) -> Callable[[CommandCallbackT], SubCommandMethod]:
    """Creates a new sub-command and associates it with the decorated function.

    Parameters
    ----------
    name : str
        The name of the sub-command.
    name_localizations : Localized | None, optional
        The sub-command name localizations.
    description : str | None, optional
        Description of the sub-command.
    description_localizations : Localized | None, optional
        The sub-command description localizations.
    options : Sequence[Option] | None, optional
        The sub-command options.

    Returns
    -------
    Callable[[CommandCallbackT], SubCommandMethod]
        A decorator that wraps the command function and returns a SubCommandMethod instance.
    """

    def decorator(func: CommandCallbackT) -> SubCommandMethod:
        command = SubCommand(
            name=name,
            name_localizations=name_localizations,
            description=description,
            description_localizations=description_localizations,
            options=options,
            sub_command_group=None,
            sub_commands={},
        )
        return SubCommandMethod(func=func, command=command)

    return decorator
