from abc import ABC, abstractmethod
from typing import Any, Dict, List


class ITranslationEngine(ABC):
    @abstractmethod
    async def start(self): ...

    @abstractmethod
    def get(
        self, key: str, *, arguments: Dict[str, Any]
    ) -> str | List[str] | Dict[str, Any] | None: ...
