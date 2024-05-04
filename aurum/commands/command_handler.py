from collections.abc import Sequence

from hikari.events import Event

from aurum.abc.hook import Hook


class CommandHandler:
    def __init__(
        self,
        allow_unknown_interactions: bool = False,
        pre_command_hooks: Sequence[Hook] | None = None,
        post_command_hooks: Sequence[Hook] | None = None,
    ) -> None:
        self.allow_unknown_interactions: bool = allow_unknown_interactions
        self.pre_command_hooks: Sequence[Hook] | None = pre_command_hooks
        self.post_command_hooks: Sequence[Hook] | None = post_command_hooks

        self.commands: None = None

    async def sync(self, _: Event) -> None:
        ...
