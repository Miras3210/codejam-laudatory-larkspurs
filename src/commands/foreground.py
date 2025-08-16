from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from utils.color import create_color

if TYPE_CHECKING:
    from terminal import Terminal


class Foreground(BaseCommand):
    """Sets the foreground color for use in drawing commands.

    @author Philip
    """

    name: str = "fg"
    help_pages: tuple[str, ...] = (
        """Sets the foreground color for use in drawing commands.

        Usage: fg color
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str, **_options: str) -> bool:
        """Set the foreground color for use in drawing commands.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: True if command was executed successfully.

        @author Philip
        """
        try:
            color = create_color(" ".join(args))
        except ValueError as e:
            terminal.output_error(e.args[0])
            return False

        terminal.foreground_color = color

        return True

    def predict_args(self, terminal: "Terminal", *args: str, **_options: str) -> str | None:
        """Predicts the next argument for help.

        :param terminal: The terminal instance.
        :param args: Arguments already passed to the command.
        :return: The predicted continuance of the arguments for the command. If new argument, start with space.
                 If no more arguments "". If error in arguments, return None.

        @author Philip
        """
        if not all(arg.isdigit() for arg in args):
            return ""

        match len(args):
            case 0:
                return " " + terminal.background_color.r
            case 1:
                return " " + terminal.background_color.g
            case 2:
                return " " + terminal.background_color.b
            case 3:
                return " " + terminal.background_color.a

        return None
