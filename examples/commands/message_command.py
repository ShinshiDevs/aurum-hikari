from hikari import GatewayBot, Message

from aurum import Client, InteractionContext, MessageCommand

bot = GatewayBot("...")
client = Client(bot)


@client.include
class ReverseTextCommand(MessageCommand):
    def __init__(self) -> None:
        super().__init__(name="Reverse", is_dm_enabled=True)

    async def callback(self, context: InteractionContext, message: Message) -> None:
        if content := message.content:
            return await context.create_response(content[::-1], ephemeral=True)
        return await context.create_response("This message don't have content", ephemeral=True)


if __name__ == "__main__":
    bot.run()
