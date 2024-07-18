import enum

from hikari.interactions import CommandInteraction, ComponentInteraction
from hikari.snowflakes import Snowflake


class BucketType(int, enum.Enum):
    """Bucket for specifying the cooldown scope"""

    USER = 0
    MEMBER = 1
    GUILD = 2

    def __getitem__(self, interaction: CommandInteraction | ComponentInteraction) -> Snowflake:
        return {
            BucketType.USER: interaction.user.id,
            BucketType.MEMBER: interaction.member.id if interaction.member else None,
            BucketType.GUILD: interaction.guild_id,
        }[self] or interaction.user.id
