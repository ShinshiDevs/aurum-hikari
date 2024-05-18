import typing

from aurum.l10n.localized import Localized


T = typing.TypeVar("T", covariant=True)
LocalizedOr = typing.Union[Localized, T]
