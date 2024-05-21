from __future__ import annotations

import typing

from hikari.commands import CommandChoice, CommandOption

from aurum.l10n.localized import Localized
from aurum.l10n.types import LocalizedOr

if typing.TYPE_CHECKING:
    from aurum.l10n import LocalizationProviderInterface
    from aurum.options import Choice, Option


def build_choice(choice: Choice, l10n: LocalizationProviderInterface) -> CommandChoice:
    return CommandChoice(
        name=str(choice.name),  # TODO: display name
        value=choice.value,
    )


def build_option(option: Option, l10n: LocalizationProviderInterface) -> CommandOption:
    description: LocalizedOr[str] = option.description or "No description"
    return CommandOption(
        type=option.type,
        name=str(option.name),
        description=str(description),
        description_localizations=(
            l10n.build_localized(description) if isinstance(description, Localized) else {}
        ),
        choices=[build_choice(choice, l10n) for choice in option.choices],
        is_required=option.is_required,
        max_length=option.max_length,
        min_length=option.min_length,
        max_value=option.max_value,
        min_value=option.min_value,
        channel_types=option.channel_types,
    )
