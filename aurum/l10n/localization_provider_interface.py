import typing

from aurum.l10n.types import Localized


class LocalizationProviderInterface(typing.Protocol):
    async def start(self) -> None: ...

    def build_localized(self, value: Localized) -> typing.Dict[str, str]: ...
