<div align="center">
    <div>
        <div align=left>
            <h1>
                <img src="docs/assets/logo.svg" width=25> Aurum
            </h1>
            <p>
                <a href="https://shinshidevs.github.io/aurum-hikari/">Documentation</a>
                ·
                <a href="https://github.com/ShinshiDevs/aurum-hikari/releases">Releases</a>
                ·
                <a href="https://pypi.org/project/aurum-hikari/">PyPI</a>
                ·
                <a href="./LICENSE">License</a>
            </p>
            <p>
                <a href="https://github.com/hikari-py/hikari">
                    <img alt="Static Badge" src="https://img.shields.io/badge/Powered%20by-hikari-E440C1">
                </a>
                <a href="https://pypi.org/project/aurum-hikari/">
                    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/aurum-hikari">
                    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/aurum-hikari">
                    <img alt="PyPI - Status" src="https://img.shields.io/pypi/status/aurum-hikari">
                </a>
                <a href="https://github.com/ShinshiDevs/aurum-hikari">
                    <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/w/ShinshiDevs/aurum-hikari">
                    <img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues-closed/ShinshiDevs/aurum-hikari">
                    <img alt="GitHub License" src="https://img.shields.io/github/license/ShinshiDevs/aurum-hikari">
                </a>
            </p>
            <p>
                <text>A flexible framework for handling commands and components with integrations.</text>
            </p>
            <p>
                <text>
                    The main purpose of this library is to help you create a bot and implement its functionality. It makes the process simpler and easier.
                </text>
                <text>
                    Our goal is to provide you, as developers, with complete freedom of action and to highlight the benefits of Hikari.
                </text>
            </p>
        </div>
    </div>
</div>

# Installation
> [!NOTE]
> Aurum requires Python 3.10 or higher.

Run command:
```md
pip install aurum-hikari
# Or
python -m pip install aurum-hikari # for unix-type systems
py -m pip install aurum-hikari # for windows
# You can use the -U flag with the `install` command (e.g., `pip install -U ...`) to update a package.
```

# Usage
```py
from hikari import GatewayBot

from aurum import Client, SlashCommand, callback

bot = GatewayBot("...")
client = Client(bot)


@client.include
class HelloCommand(SlashCommand):
    def __init__(self) -> None:
        super().__init__(name="hello", description="Say hi to bot")

    async def callback(self, context: InteractionContext) -> None:
        await context.create_response(f"Hi, {context.user.mention}!")


if __name__ == "__main__":
    client.run()
```
More in [examples folder](./examples).

# Projects
So far, no one has been using our library.

# Contributing
Not available yet.

# Issues and bugs
If you find any errors in the library, please let us know about them on the [issues Github page](https://github.com/ShinshiDevs/aurum-hikari/issues). Thanks!

# Inspiration
- [hikari-crescent](https://github.com/hikari-crescent/hikari-crescent) - A command handler for Hikari that keeps your project neat and tidy.
