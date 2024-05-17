import typing

from aurum.internal.exceptions.base_exception import AurumException


class UnknownCommandException(AurumException):
    """Occurs when the command wasn't found."""

    def __init__(self, *command_name: str) -> None:
        names: typing.List[str] = list(command_name)
        message: str = f"Cannot access command with name {names.pop()}"
        for name in names:
            message += f" of {name}"
        super().__init__(message)
