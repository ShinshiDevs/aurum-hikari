from hikari import GatewayBot, OptionType

from aurum import Client, InteractionContext, SlashCommand
from aurum.commands.decorators import sub_command
from aurum.options import Option

bot = GatewayBot("...")
client = Client(bot)


@client.include
class TextCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__("text", is_dm_enabled=True)

    @sub_command(
        name="reverse",
        description="Reverse string",
        options=[Option(type=OptionType.STRING, name="string", description="String to reverse")],
    )
    async def reverse(self, context: InteractionContext, string: str) -> None:
        return await context.create_response(string[::-1], ephemeral=True)

    @sub_command(
        name="uppercase",
        description="Convert string to uppercase",
        options=[Option(type=OptionType.STRING, name="string", description="String to convert")],
    )
    async def uppercase(self, context: InteractionContext, string: str) -> None:
        await context.create_response(string.upper(), ephemeral=True)

    @sub_command(
        name="lowercase",
        description="Convert string to lowercase",
        options=[Option(type=OptionType.STRING, name="string", description="String to convert")],
    )
    async def lowercase(self, context: InteractionContext, string: str) -> None:
        await context.create_response(string.lower(), ephemeral=True)


if __name__ == "__main__":
    bot.run()
