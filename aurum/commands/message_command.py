from __future__ import annotations

import typing

from aurum.commands.context_menu_command import ContextMenuCommand

if typing.TYPE_CHECKING:
    from hikari.messages import Message

    from aurum.interactions import InteractionContext


class MessageCommand(ContextMenuCommand):
    """
    Represents a message-command.

    Raises:
        NotImplementedError: This method should be overridden in a subclass and will raise an exception if called directly.
    """

    async def callback(self, context: InteractionContext, message: Message) -> None:
        raise NotImplementedError()
