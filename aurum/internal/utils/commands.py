from hikari.commands import CommandChoice, CommandOption

from aurum.l10n import LocalizationProviderInterface, Localized
from aurum.options import Choice, Option


def build_option(option: Option, l10n: LocalizationProviderInterface | None) -> CommandOption:
    if l10n and isinstance(option.description, Localized):
        l10n.build_localized(option.description)
    if l10n and isinstance(option.display_name, Localized):
        l10n.build_localized(option.display_name)
    return CommandOption(
        type=option.type,
        name=option.name,
        name_localizations=getattr(option.display_name, "value", {}),
        description=str(option.description),
        description_localizations=getattr(option.description, "value", {}),
        choices=[build_choice(choice, l10n) for choice in option.choices],
        is_required=option.is_required,
        max_length=option.max_length,
        min_length=option.min_length,
        max_value=option.max_value,
        min_value=option.min_value,
        channel_types=option.channel_types,
    )


def build_choice(choice: Choice, l10n: LocalizationProviderInterface | None) -> CommandChoice:
    if l10n and isinstance(choice.name, Localized):
        l10n.build_localized(choice.name)
    return CommandChoice(
        name=str(choice.name),
        name_localizations=getattr(choice.name, "value", {}),
        value=choice.value,
    )
