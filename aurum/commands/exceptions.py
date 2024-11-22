from typing import Any

from aurum.exceptions import AurumException


class BaseCommandException(AurumException):
    """Base exception class for command related errors.

    Parameters
    ----------
    command_name : str
        Name of the command that caused the error.
    *args : Any
            Positional arguments to be passed to the parent exception class.
    **kwargs : Any
        Keyword arguments to be passed to the parent exception class.

    Attributes
    ----------
    command_name : str
        The name of the command associated with this exception,
        stored as an instance attribute.
    """

    def __init__(self, command_name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.command_name: str = command_name


class CommandCallbackNotImplemented(BaseCommandException):
    """Exception raised when a command callback is not implemented.

    Parameters
    ----------
    command_name : str
        Name of the command with missing callback implementation.
    """

    def __init__(self, command_name: str) -> None:
        super().__init__(command_name, f"Callback for command {command_name} is not implemented or not set.")


class CommandNotFound(BaseCommandException):
    """Exception raised when a command is not found.

    Parameters
    ----------
    command_name : str
        Name of the command that was not found.
    """

    def __init__(self, command_name: str) -> None:
        super().__init__(command_name, f"Command {command_name} is not found.")


class SubCommandNotFound(BaseCommandException):
    """Exception raised when a subcommand is not found.

    Parameters
    ----------
    command_name : str
        Name of the base command.
    *sub_commands : str
        Variable number of subcommand names that were not found.
    """

    def __init__(self, command_name: str, *sub_commands: str) -> None:
        super().__init__(
            command_name,
            f"Command {command_name} {" ".join(sub_command for sub_command in sub_commands if sub_command)} is not found.",
        )
