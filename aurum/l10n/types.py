from dataclasses import dataclass
from typing import Any, Mapping, TypeVar, Union


@dataclass(slots=True)
class Localized:
    key: str | None = None
    fallback: str | None = None

    def __str__(self) -> str:
        return str(self.fallback)


@dataclass
class Locale:
    name: str
    value: Mapping[str, Any]


T = TypeVar("T", covariant=True)
LocalizedOr = Union[Localized, T]
