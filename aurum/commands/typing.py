from collections.abc import Callable, Coroutine
from typing import TYPE_CHECKING, Any, Dict, TypeVar

from aurum.option import Option

if TYPE_CHECKING:
    from aurum.commands.sub_command import SubCommand

CommandCallbackT = TypeVar("CommandCallbackT", bound=Callable[..., Coroutine[None, None, Any]])

SubCommandsDictT = TypeVar("SubCommandsDictT", bound=Dict[str, "SubCommand"])
AutocompletesDictT = TypeVar("AutocompletesDictT", bound=Dict[str, Option])
