import os
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict
from logging import getLogger

from aurum.abc.i18n import ITranslationEngine

if TYPE_CHECKING:
    from logging import Logger


class DefaultTranslationEngine(ITranslationEngine):
    def __init__(self, base_directory: os.PathLike[str]) -> None:
        self.__logger: Logger = getLogger("aurum.i18n")
        self.base_directory: Path = Path(base_directory)
        self.languages: Dict[str, Any] = {}
