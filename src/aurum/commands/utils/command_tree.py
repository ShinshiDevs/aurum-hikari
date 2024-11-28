from collections.abc import Sequence

from hikari.commands import OptionType, PartialCommand, SlashCommand


def build_command_tree(commands: Sequence[PartialCommand], indent: str = "\t") -> str:
    tree: list[str] = []
    for command in commands:
        tree.append(f"{indent}{command.name}")
        if isinstance(command, SlashCommand) and command.options:
            for option in command.options:
                if option.type == OptionType.SUB_COMMAND_GROUP:
                    tree.append(f"{indent * 2}{option.name}")

                    for option in option.options or ():
                        tree.append(f"{indent * 3}{option.name}")
                elif option.type == OptionType.SUB_COMMAND:
                    tree.append(f"{indent * 2}{option.name}")
    return "\n".join(tree)
