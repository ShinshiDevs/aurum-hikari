from hikari import GatewayBot

from aurum import Client, InteractionContext, SlashCommand

bot = GatewayBot("...")
client = Client(bot)


@client.include
class PingCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__("ping", is_dm_enabled=True)

    async def callback(self, context: InteractionContext) -> None:
        await context.create_response(
            f":ping_pong: Pong! `{context.bot.heartbeat_latency*1_000:.0f}ms`"
        )


if __name__ == "__main__":
    bot.run()
