from __future__ import annotations

import typing

from aurum.internal.consts import SUB_COMMANDS_VAR
from aurum.commands.sub_commands import SubCommand


class SlashCommandMeta(type):
    def __new__(
        mcs: typing.Type[SlashCommandMeta],
        name: str,
        bases: typing.Tuple[type, ...],
        attrs: typing.Dict[str, typing.Any],
    ) -> SlashCommandMeta:
        cls: SlashCommandMeta = super().__new__(mcs, name, bases, attrs)
        setattr(cls, SUB_COMMANDS_VAR, {})
        for name, obj in attrs.items():
            if isinstance(obj, SubCommand):
                getattr(cls, SUB_COMMANDS_VAR)[obj.name] = obj
        return cls
