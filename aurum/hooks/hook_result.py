from dataclasses import dataclass


@dataclass
class HookResult:
    stop: bool = False
