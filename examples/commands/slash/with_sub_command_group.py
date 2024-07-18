import datetime
from typing import TypedDict

from hikari import (
    ChannelType,
    GatewayBot,
    OptionType,
    PartialChannel,
    TextableGuildChannel,
)

from aurum import Client, InteractionContext, Option, SlashCommand, sub_command

bot = GatewayBot("...")
client = Client(bot)


class Statistic(TypedDict):
    name: str
    date: datetime.datetime
    count: int


@client.include
class StatsCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__("stats")

    @sub_command("channel")
    async def channel(self, context: InteractionContext) -> None: ...

    @channel.sub_command(
        "messages",
        description="Message statistic for channel",
        options=[
            Option(
                type=OptionType.CHANNEL,
                name="channel",
                description="Of channel",
                channel_types=[ChannelType.GUILD_TEXT],
                is_required=False,
            )
        ],
    )
    async def channel_messages(
        self, context: InteractionContext, channel: PartialChannel | None = None
    ) -> None:
        channel = await context.bot.rest.fetch_channel(channel) if channel else context.channel
        assert isinstance(channel, TextableGuildChannel)
        now: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        data: dict[str, Statistic] = {
            "last_hour": Statistic(
                name="Last hour", date=now - datetime.timedelta(hours=1), count=0
            ),
            "last_12_h": Statistic(
                name="Last 12 hours", date=now - datetime.timedelta(hours=12), count=0
            ),
            "last_24_h": Statistic(
                name="Last 24 hours", date=now - datetime.timedelta(hours=24), count=0
            ),
        }
        async for message in channel.fetch_history(after=data["last_24_h"]["date"]):
            for value in data.values():
                if message.created_at > value["date"]:
                    value["count"] += 1
        await context.create_response(
            f"**Message statistic for {channel.mention}**\n"
            + "\n".join(
                [f"{statistic['name']}: {statistic['count']}" for statistic in data.values()]
            )
        )


if __name__ == "__main__":
    bot.run()
