from collections.abc import Callable, Coroutine
from typing import TYPE_CHECKING, Any, Dict

from aurum.option import Option

if TYPE_CHECKING:
    from aurum.commands.sub_command import SubCommand

CommandCallbackT = Callable[..., Coroutine[None, None, Any]]
SubCommandsDictT = Dict[str, "SubCommand"]
AutocompletesDictT = Dict[str, Option]
