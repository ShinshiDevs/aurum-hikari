from dataclasses import dataclass
from typing import TypeVar, Union


@dataclass(slots=True)
class Localized:
    key: str | None = None
    fallback: str | None = None


T = TypeVar("T", covariant=True)
LocalizedOr = Union[Localized, T]
