from typing import Any

from hikari.commands import OptionType
from hikari.interactions import CommandInteraction, CommandInteractionOption
from hikari.snowflakes import Snowflake


def resolve_interaction_option(interaction: CommandInteraction, option: CommandInteractionOption) -> Any:
    if not interaction.resolved or not isinstance(option.value, Snowflake):
        return option.value
    value = Snowflake(option.value)
    match option.type:
        case OptionType.USER:
            return interaction.resolved.members.get(value, interaction.resolved.users.get(value))
        case OptionType.CHANNEL:
            return interaction.resolved.channels.get(value)
        case OptionType.ROLE:
            return interaction.resolved.roles.get(value)
        case OptionType.MENTIONABLE:
            return interaction.resolved.members.get(value, interaction.resolved.roles.get(value))
        case OptionType.ATTACHMENT:
            return interaction.resolved.attachments.get(value)
        case _:
            return None
