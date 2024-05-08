import asyncio
from collections.abc import Sequence
from typing import Any, List

from hikari.events import InteractionCreateEvent, StartedEvent, StartingEvent
from hikari.impl.gateway_bot import GatewayBot
from hikari.interactions import CommandInteraction, PartialInteraction
from hikari.snowflakes import Snowflakeish

from aurum.commands.command_handler import CommandHandler
from aurum.errors import ErrorHandler
from aurum.i18n import ILocalizationEngine


class Client:
    def __init__(
        self,
        bot: GatewayBot,
        *,
        l10n: ILocalizationEngine,
        model: Any = None,
        default_guild: Snowflakeish | None = None,
        sync_commands: bool = True,
        error_handler: ErrorHandler | None = None,
        suppress_unknown_interaction_warning: bool = False,
    ) -> None:
        self._starting_tasks: List[asyncio.Task] = []

        self.bot: GatewayBot = bot
        self.l10n: ILocalizationEngine = l10n
        self.model: Any = model

        self.sync_commands: bool = sync_commands
        self.commands: CommandHandler = CommandHandler()

        self._starting_tasks.append(asyncio.create_task(l10n.start()))

    async def execute_all_tasks(self, tasks: Sequence[asyncio.Task]) -> None:
        for task in tasks:
            await task

    async def on_starting_event(self, _: StartingEvent) -> None:
        await self.execute_all_tasks(self._starting_tasks)

    async def on_started_event(self, _: StartedEvent) -> None:
        if self.sync_commands:
            await self.commands.sync()

    async def on_interaction(self, event: InteractionCreateEvent) -> None:
        interaction: PartialInteraction = event.interaction
        if isinstance(interaction, CommandInteraction):
            await self.commands.process(interaction)
