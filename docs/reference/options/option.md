::: aurum.options.option

### Example
```{.py3 hl_lines="9-14"}
class UserCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__(name="user")

    @sub_command(
        name="info",
        description="Get information about user",
        options=[
            Option(
                type=OptionType.USER,
                name="user",
                description="About who you want to know (or put an ID)",
                is_required=False,
            )
        ],
    )
    async def user_info(
        self, context: InteractionContext, user: InteractionMember | User | None = None
    ) -> None:
        if not user:
            user = context.interaction.user
        return await context.create_response(
            content=f"User **\@{user.username}**\ncreated at: <t:{round(user.created_at.timestamp())}:R>\nID: {user.id}"
        )
```
