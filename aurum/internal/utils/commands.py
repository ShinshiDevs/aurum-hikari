from __future__ import annotations

import typing

from hikari.commands import CommandChoice, CommandOption

if typing.TYPE_CHECKING:
    from aurum.l10n import LocalizationProviderInterface
    from aurum.options import Choice, Option


def build_choice(choice: Choice, l10n: LocalizationProviderInterface) -> CommandChoice:
    return CommandChoice(
        name=str(choice.name),
        name_localizations=l10n.build_localized(choice.name),
        value=choice.value,
    )


def build_option(option: Option, l10n: LocalizationProviderInterface) -> CommandOption:
    return CommandOption(
        type=option.type,
        name=str(option.name),
        name_localizations=l10n.build_localized(option.name),
        description=str(option.description),
        description_localizations=l10n.build_localized(option.description),
        choices=[build_choice(choice, l10n) for choice in option.choices],
        is_required=option.is_required,
        max_length=option.max_length,
        min_length=option.min_length,
        max_value=option.max_value,
        min_value=option.min_value,
        channel_types=option.channel_types,
    )
