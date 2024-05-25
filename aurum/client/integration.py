from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from aurum.client import Client


class IClientIntegration(typing.Protocol):
    """Interface of integration for base client

    Important:
        If your integration add new variables to client,
        you must override the client class and add some new variables.

        !!! example
            ```py
            class Client(aurum.Client):
                def __init__(self, **kwargs) -> None:
                    self.new_variable: VariableType | None = None
                    super().__init__(**kwargs)
            ```
    """

    def install(self, client: Client) -> None:
        """Integration install script"""
        ...
