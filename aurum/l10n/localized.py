from typing import Any, Dict

import attrs


@attrs.define(kw_only=True, hash=False, weakref_slot=False)
class Localized:
    value: str | Dict[str, Any]
    """Key.
    
    After building it will be replaced by translations.
    Look out [fallback][aurum.l10n.localized.Localized.fallback] for more information.
    """

    fallback: str | None = None
    """
    You should use this in your localization provider `build_localized` function,
    because...
    ```py
    #   Localized(value="commands.hi.description", fallback=None)
    
    LocalizationProvider.build_localized(Localized)
    
    # For example.
    # There is `build_localized` will put a first translation into fallback.
    # But you can do anything you want.
    #
    #   Localized(value={"ro": "Salutați botul", "lt": "Pasisveikinkite su botu"}, fallback="Salutați botul")
    #
    # And fallback will be used for default description (for example) of command
    # and value for description_localizations of command.
    """

    def __str__(self) -> str:
        return str(self.fallback)
