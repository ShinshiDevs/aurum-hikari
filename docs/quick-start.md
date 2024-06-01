---
title: Quick start
---

# :octicons-rocket-24: Quick start

### Installation

!!! note
    Aurum requires Python 3.10 or higher.

Run command `pip install (1) aurum-hikari` or:
{ .annotate }

1. You can use the -U flag with the `install` command (e.g., `pip install -U ...`) to update a package.

=== "Unix" 
    `python3 -m pip install (1) aurum-hikari`
    { .annotate }
    
    1. You can use the -U flag with the `install` command (e.g., `pip install -U ...`) to update a package.

=== "Windows"
    `py -m pip install (1) aurum-hikari`
    { .annotate }
    
    1. You can use the -U flag with the `install` command (e.g., `pip install -U ...`) to update a package.

### How to
#### Create a command
##### Slash command
You need to import the [SlashCommand class][aurum.commands.slash_command.SlashCommand] and inherit from it.
!!! example
    === "With callback"
        ```py
        class HelloCommand(SlashCommand):
            def __init__(self) -> None:
                super().__init__(name="hello", description="Say hi to bot")  # (1)
    
            async def callback(self, context: InteractionContext) -> None:
                await context.create_response(f"Hi, {context.user.mention}!")
        ```

        1. Base information about your command: name, description, default member permissions and etc.

    === "With sub-commands"
        ```py
        class ABCCommand(SlashCommand):  # (1)
            def __init__(self) -> None:
                super().__init__(name="a")  # (2)

            @sub_command(name="b")  # (3)
            async def b_command(self, context: InteractionContext) -> None:
                ...  # (4)

            @b_command.sub_command(name="c")
            async def b_c_command(self, context: InteractionContext) -> None:
                ...
        ```
        
        1. When command has a sub-commands, callback will be ignored.
        2. Base information about your command: name, description, default member permissions and etc.
        3. Base information about your sub-command. The same fields with slash-command, but without guild, default member permissions, is nsfw, dm enabled flags.
        4. If sub-command have another sub-command, callback of parent sub-command will be ignored too.

* * *

##### User command
!!! note
    User command this an application command in user's context menu.
You need to import the [UserCommand class][aurum.commands.user_command.UserCommand] and inherit from it.
!!! example
    ```py
    class HelloUserCommand(UserCommand):
        def __init__(self) -> None:
            super().__init__(name="Hello to")

        async def callback(self, context: InteractionContext, target: InteractionMember | User) -> None:
            await context.create_response(f"Hi, {target.mention}!")
    ```

* * *

##### Message command
!!! note
    User command this an application command in message's context menu.
You need to import the [MessageCommand class][aurum.commands.message_command.MessageCommand] and inherit from it.
!!! example
    ```py
    class ReverseTextCommand(MessageCommand):
        def __init__(self) -> None:
            super().__init__(name="Reverse", dm_enabled=True)

        async def callback(self, context: InteractionContext, message: Message) -> None:
            await context.create_response(message.content[::-1])
    ```

* * *


#### Work with plugins
Look out a [plugins integration](reference/integrations/plugins.md).

#### Work with components
Sadly, but at the moment Aurum don't have a components. :octicons-clock-fill-24:
