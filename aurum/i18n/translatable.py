from dataclasses import dataclass

from hikari.undefined import UndefinedType


@dataclass
class Translatable:
    key: str | UndefinedType | None = None
    fallback: str | None = None
