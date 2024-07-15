from collections.abc import Sequence

from hikari import AutocompleteInteractionOption, GatewayBot, OptionType

from aurum import Client, InteractionContext, SlashCommand
from aurum.autocomplete import AutocompleteChoice
from aurum.context import AutocompleteContext
from aurum.option import Option

bot = GatewayBot("...")
client = Client(bot)

languages: list[str] = [
    "Python",
    "JavaScript",
    "TypeScript",
    "Java",
    "C",
    "Rust",
]


@client.include
class LanguagesCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__(
            "languages",
            options=[
                Option(
                    type=OptionType.STRING,
                    name="language",
                    autocomplete=self.languages_autocomplete,
                )
            ],
        )

    @staticmethod
    async def languages_autocomplete(
        _: AutocompleteContext, option: AutocompleteInteractionOption
    ) -> Sequence[AutocompleteChoice]:
        return list(
            AutocompleteChoice(name=language, value=language.lower())
            for language in languages
            if str(option.value).lower() in language.lower()
        )

    async def callback(self, context: InteractionContext, language: str) -> None:
        return await context.create_response(f"You have choiced {language}!")


if __name__ == "__main__":
    bot.run()
