from __future__ import annotations

__all__: Sequence[str] = ("Cooldown", "cooldown", "BucketType")

from collections.abc import Sequence

from .bucket import BucketType
from .hook import Cooldown, cooldown
