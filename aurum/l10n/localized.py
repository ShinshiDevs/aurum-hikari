from dataclasses import dataclass


@dataclass(slots=True)
class Localized:
    """Placeholder for `key` and `fallback` values"""

    key: str | None = None
    fallback: str | None = None

    def __str__(self) -> str:
        return str(self.fallback)
