from dataclasses import dataclass


@dataclass(slots=True)
class Translatable:
    key: str | None = None
    fallback: str | None = None
