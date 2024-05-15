from __future__ import annotations

import typing

from hikari.events import InteractionCreateEvent

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

    from hikari.impl import GatewayBot

    from aurum.commands.command_handler import CommandHandler

type ComponentHandler = None  # TODO: Remove that, when ComponentHandler will appear


class InteractionProcessor:
    __slots__: Sequence[str] = ("bot", "commands", "components", "ignore_unknown_interactions")

    def __init__(
        self,
        bot: GatewayBot,
        commands: CommandHandler,
        components: ComponentHandler,
        ignore_unknown_interactions: bool,
    ) -> None:
        self.bot: GatewayBot = bot

        self.commands: CommandHandler = commands
        self.components: ComponentHandler = components

        self.ignore_unknown_interactions: bool = ignore_unknown_interactions

    async def on_interaction(
        self, event: InteractionCreateEvent
    ) -> None: ...  # TODO: Interaction proceed
