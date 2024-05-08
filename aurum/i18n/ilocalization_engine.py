from typing import Protocol


class ILocalizationEngine(Protocol):
    async def start(self) -> None: ...
