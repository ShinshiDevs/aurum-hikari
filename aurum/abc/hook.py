from abc import ABC, abstractmethod

from aurum.hook_result import HookResult


class Hook(ABC):
    @abstractmethod
    async def callback(self) -> HookResult:
        ...
