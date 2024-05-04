from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class HookResult:
    stop: bool = False

    extra: Dict[str, Any] = field(default_factory=dict)
    """Any extra information for this hook result"""
