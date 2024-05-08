from hikari import UNDEFINED

from aurum.i18n.translatable import Translatable


def cast_translatable(value: Translatable | str) -> Translatable:
    return (
        value
        if isinstance(value, Translatable)
        else Translatable(key=UNDEFINED, fallback=value)
    )
