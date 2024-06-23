from typing import TypeVar, Union

from aurum.l10n.localized import Localized

T = TypeVar("T", covariant=True)
LocalizedOr = Union["Localized", T]
