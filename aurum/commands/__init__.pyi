# DO NOT MANUALLY EDIT THIS FILE!
# This file was automatically generated by `nox -s generate_stubs`

from aurum.commands.base_command import BaseCommand as BaseCommand
from aurum.commands.context_menu_command import ContextMenuCommand as ContextMenuCommand
from aurum.commands.exceptions import BaseCommandException as BaseCommandException
from aurum.commands.exceptions import CommandCallbackNotImplemented as CommandCallbackNotImplemented
from aurum.commands.exceptions import CommandNotFound as CommandNotFound
from aurum.commands.exceptions import SubCommandNotFound as SubCommandNotFound
from aurum.commands.options import Choice as Choice
from aurum.commands.options import Option as Option
from aurum.commands.slash_command import SlashCommand as SlashCommand
from aurum.commands.slash_command import SlashCommandGroup as SlashCommandGroup
from aurum.commands.sub_command import SubCommand as SubCommand
from aurum.commands.types import Localized as Localized

__all__ = [
    "BaseCommand",
    "ContextMenuCommand",
    "BaseCommandException",
    "CommandNotFound",
    "SubCommandNotFound",
    "CommandCallbackNotImplemented",
    "Option",
    "Choice",
    "SlashCommand",
    "SlashCommandGroup",
    "SubCommand",
    "Localized",
]
