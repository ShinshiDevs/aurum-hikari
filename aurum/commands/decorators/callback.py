from typing import Any

from aurum.commands.constants import COMMAND_CALLBACK_FLAG
from aurum.commands.typing import CommandCallbackT


def callback(func: CommandCallbackT) -> CommandCallbackT:
    def wrapper(*args, **kwargs) -> Any:
        return func(*args, **kwargs)

    setattr(wrapper, COMMAND_CALLBACK_FLAG, True)
    return wrapper
