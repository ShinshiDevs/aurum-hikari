import typing
from dataclasses import dataclass


@dataclass
class Locale:
    """Locale"""

    name: str
    value: typing.Dict[str, typing.Any]
