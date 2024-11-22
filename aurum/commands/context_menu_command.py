from abc import abstractmethod

from hikari.messages import Message
from hikari.users import PartialUser

from aurum.commands.base_command import BaseCommand
from aurum.context import InteractionContext


class ContextMenuCommand(BaseCommand):
    """Base class for context menu commands.

    Notes
    -----
    This is an abstract base class that should be subclassed by specific context menu command types.
    """


class MessageCommand(ContextMenuCommand):
    """Class for handling message context menu commands.

    Parameters
    ----------
    context : InteractionContext
        The interaction context for the command.
    message : Message
        The message that the context menu was triggered on.

    Notes
    -----
    Subclasses must implement the abstract callback method to define the command's behavior.
    """

    @abstractmethod
    async def callback(self, context: InteractionContext, message: Message) -> None: ...


class UserCommand(ContextMenuCommand):
    """Class for handling user context menu commands.

    Parameters
    ----------
    context : InteractionContext
        The interaction context for the command.
    user : PartialUser
        The user that the context menu was triggered on.

    Notes
    -----
    Subclasses must implement the abstract callback method to define the command's behavior.
    """

    @abstractmethod
    async def callback(self, context: InteractionContext, user: PartialUser) -> None: ...
