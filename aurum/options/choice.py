from dataclasses import dataclass

from aurum.i18n.translatable import Translatable


@dataclass(kw_only=True, slots=True)
class Choice:
    name: Translatable | str
    value: str | float | int
