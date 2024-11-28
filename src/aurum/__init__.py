"""Aurum is a flexible framework for handling commands and components."""

from collections.abc import Sequence

from aurum.commands.base_command import BaseCommand
from aurum.commands.context_menu_command import MessageCommand, UserCommand
from aurum.commands.decorators.sub_command import sub_command
from aurum.commands.exceptions import (
    BaseCommandException,
    CommandCallbackNotImplemented,
    CommandNotFound,
    SubCommandNotFound,
)
from aurum.commands.impl.command_builder import CommandBuilder
from aurum.commands.impl.command_handler import CommandHandler
from aurum.commands.options import Choice, Option
from aurum.commands.slash_command import SlashCommand, SlashCommandGroup
from aurum.commands.sub_command import SubCommand, SubCommandMethod
from aurum.context import InteractionContext
from aurum.exceptions import AurumException

__all__: Sequence[str] = (
    "InteractionContext",
    "AurumException",
    "BaseCommand",
    "MessageCommand",
    "UserCommand",
    "BaseCommandException",
    "CommandCallbackNotImplemented",
    "CommandNotFound",
    "SubCommandNotFound",
    "Choice",
    "Option",
    "SlashCommand",
    "SlashCommandGroup",
    "SubCommandMethod",
    "SubCommand",
    "sub_command",
    "CommandHandler",
    "CommandBuilder",
)
