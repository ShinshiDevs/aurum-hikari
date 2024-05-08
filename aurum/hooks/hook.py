from typing import Protocol

from aurum.hooks.hook_result import HookResult
from aurum.interaction import InteractionContext


class Hook(Protocol):
    async def callback(self, context: InteractionContext) -> HookResult: ...
