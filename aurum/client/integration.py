from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from aurum.client import Client


class IClientIntegration(typing.Protocol):
    """Interface of integration for base client"""

    def install(self, client: Client) -> None:
        """Integration install script"""
        ...
