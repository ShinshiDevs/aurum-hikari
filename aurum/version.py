from typing import NamedTuple


class Version(NamedTuple):
    major: int
    minor: int
    subminor: int
    build: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.subminor}.{self.build}"
