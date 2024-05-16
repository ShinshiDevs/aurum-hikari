from __future__ import annotations

import typing
from dataclasses import dataclass, field

from aurum.options import Option

if typing.TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Sequence

    from aurum.l10n.types import LocalizedOr


@dataclass(slots=True, kw_only=True)
class SubCommand:
    """
    A class representing a sub-command.

    Attributes:
        callback (Callable[..., Awaitable[Any]]): A callback of sub-command.
        name (str): The internal name of the command used for identification, display if `display_name` is not provided.
        description (LocalizedOr[str] | None): Optional description of the command for help documentation.
        display_name (LocalizedOr[str] | None): Optional localized display name of the command.
        options (Sequence[Option]): Options to the command.
        sub_commands (Dict[str, SubCommand]): Sub-commands of the sub-command.

    Methods:
        sub_command: A decorator method used to add a new sub-command to this.

    Example:
        ```py
        class ABCCommand(SlashCommand):
            def __init__(self) -> None:
                super().__init__(name="a")

            @sub_command(name="b")
            async def b_command(self, context: InteractionContext) -> None:
                ...

            @b_command.sub_command(name="c")
            async def b_c_command(self, context: InteractionContext) -> None:
                ...
        ```
    """

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
        def decorator(func: Callable[..., Awaitable[None]]) -> None:
            self.sub_commands[name] = SubCommand(
                callback=func,
                name=name,
                description=description,
                options=options,
            )

        return decorator
