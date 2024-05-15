import typing


class LocalizationProviderInterface(typing.Protocol):
    async def start(self) -> None:
        pass
