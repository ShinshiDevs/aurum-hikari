from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from aurum.l10n.localized import Localized

T = typing.TypeVar("T", covariant=True)
LocalizedOr = typing.Union["Localized", T]
