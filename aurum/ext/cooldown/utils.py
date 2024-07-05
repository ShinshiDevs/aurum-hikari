from hikari.interactions import CommandInteraction, ComponentInteraction
from hikari.snowflakes import Snowflake

from aurum.ext.cooldown.bucket import BucketType


def target_from_bucket(
    interaction: CommandInteraction | ComponentInteraction, bucket: BucketType
) -> Snowflake:
    return {
        BucketType.USER: interaction.user.id,
        BucketType.MEMBER: interaction.member.id if interaction.member else None,
        BucketType.GUILD: interaction.guild_id,
    }[bucket] or interaction.user.id
