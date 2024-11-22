from __future__ import annotations

from collections.abc import Callable, Sequence
from types import MethodType
from typing import TYPE_CHECKING

import attrs

from aurum.commands.options import Option
from aurum.commands.types import Localized
from aurum.exceptions import AurumException

if TYPE_CHECKING:
    from aurum.commands.slash_command import SlashCommandGroup
    from aurum.commands.types import CommandCallbackT


@attrs.define(kw_only=True, eq=False, weakref_slot=False, hash=True)
class SubCommandMethod:
    """Represents a method as command callback with its associated sub-command.

    This class handles the binding between command methods and their sub-command definitions.

    Parameters
    ----------
    func : CommandCallbackT
        The callback function
    command : SubCommand
        The sub-command
    """

    func: CommandCallbackT
    command: SubCommand

    def method(self, group: SlashCommandGroup) -> CommandCallbackT:
        return MethodType(self.func, group)

    def sub_command(
        self,
        name: str,
        *,
        name_localizations: Localized | None = None,
        description: str | None = None,
        description_localizations: Localized | None = None,
        options: Sequence[Option] | None = None,
    ) -> Callable[[CommandCallbackT], SubCommandMethod]:
        """Creates a new sub-command and associates it with the decorated function.

        This method creates a child sub-command that will be registered in parent command.

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
            command = self.command.add_sub_command(
                SubCommandMethod(
                    func=func,
                    command=SubCommand(
                        name=name,
                        name_localizations=name_localizations,
                        description=description,
                        description_localizations=description_localizations,
                        options=options,
                        sub_command_group=self.command,
                        sub_commands=None,
                    ),
                )
            )
            return command

        return decorator


@attrs.define(kw_only=True, eq=False, weakref_slot=False, hash=True)
class SubCommand:
    """Represents a sub-command in a command hierarchy.

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
    sub_command_group : SubCommand | None
        Parent sub-command group if this is a child command.
    sub_commands : Dict[str, SubCommandMethod] | None
        Dictionary of child sub-commands if this is a group.
    """

    name: str = attrs.field(repr=True)
    name_localizations: Localized | None = attrs.field(default=None, repr=False)
    description: str | None = attrs.field(default=None, repr=False)
    description_localizations: Localized | None = attrs.field(default=None, repr=False)

    options: Sequence[Option] | None = attrs.field(factory=tuple, repr=False)

    sub_command_group: SubCommand | None = attrs.field(default=None, repr=True)
    sub_commands: dict[str, SubCommandMethod] | None = attrs.field(default=None, repr=True)

    def add_sub_command(self, wrapper: SubCommandMethod) -> SubCommandMethod:
        if self.sub_command_group is not None:
            raise AurumException("Child of sub command group cannot have sub commands")
        if self.sub_commands is None:
            self.sub_commands = {}
        self.sub_commands[wrapper.command.name] = wrapper
        return wrapper
