from datetime import datetime

from hikari import Embed, OwnUser

from aurum import InteractionContext, SlashCommand
from aurum.ext.plugins import Plugin

plugin = Plugin("Information")


@plugin.include
class BotCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__(name="bot", description="Information about the bot")

    async def callback(self, context: InteractionContext) -> None:
        bot_user: OwnUser | None = context.bot.get_me()
        assert isinstance(bot_user, OwnUser)
        return await context.create_response(
            embed=(
                Embed(
                    title=bot_user.global_name,
                    description=(
                        f"You're on #{context.guild.shard_id} shard" if context.guild else None
                    ),
                    timestamp=datetime.fromtimestamp(datetime.now().timestamp()),
                )
                .add_field("Latency", f"{context.bot.heartbeat_latency*1_000:.0f}")
                .add_field("Guilds", f"{len(context.bot.cache.get_guilds_view())}")
                .add_field(
                    "Users",
                    f"{sum([guild.member_count for guild in context.bot.cache.get_guilds_view().values()])}",  # type: ignore
                )
                .set_footer(f"ID: {bot_user.id}")
                .set_thumbnail(bot_user.avatar_url)
            )
        )
