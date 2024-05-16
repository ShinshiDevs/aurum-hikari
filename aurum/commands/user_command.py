from __future__ import annotations

import typing

from aurum.internal.context_menu_command import ContextMenuCommand

if typing.TYPE_CHECKING:
    from hikari.interactions import InteractionMember
    from hikari.users import PartialUser

    from aurum.interactions import InteractionContext


class UserCommand(ContextMenuCommand):
    """
    Represents a user-command.

    Raises:
        NotImplementedError: This method should be overridden in a subclass and will raise an exception if called directly.
    """

    async def callback(
        self, context: InteractionContext, target: InteractionMember | PartialUser
    ) -> None:
        raise NotImplementedError()
