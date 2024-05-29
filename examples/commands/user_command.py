from hikari import GatewayBot, InteractionMember, PartialUser

from aurum import Client, InteractionContext, UserCommand

bot = GatewayBot("...")
client = Client(bot)


@client.include
class HelloUserCommand(UserCommand):
    def __init__(self) -> None:
        super().__init__(name="Hello to")

    async def callback(
        self, context: InteractionContext, target: InteractionMember | PartialUser
    ) -> None:
        await context.create_response(f"Hi, {target.mention}!")


if __name__ == "__main__":
    bot.run()
