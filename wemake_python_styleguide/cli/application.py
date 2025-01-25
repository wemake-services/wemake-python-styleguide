"""Provides WPS CLI application class."""
import functools
from argparse import Namespace
from collections.abc import Callable, Mapping
from typing import final, Any

from wemake_python_styleguide.cli.commands.base import AbstractCommand, Initialisable
from wemake_python_styleguide.cli.commands.explain.command import ExplainCommand


@final
class Application:
    """WPS CLI application class."""

    def __init__(self) -> None:
        """Create application and init commands."""
        self.commands: Mapping[str, AbstractCommand[Any]] = {
            'explain': ExplainCommand(),
        }

    def run_subcommand(self, subcommand: str, args: Namespace) -> int:
        """Run subcommand with provided arguments."""
        cmd = self.commands[subcommand]
        args_dict = vars(args)  # noqa: WPS421
        args_dict.pop('func')  # argument classes do not expect that
        cmd_args = cmd.args_type(**args_dict)
        return cmd.run(cmd_args)

    def curry_run_subcommand(
        self, subcommand: str
    ) -> Callable[[Namespace], int]:
        """Helper func for easy use of argparse config."""
        return functools.partial(self.run_subcommand, subcommand=subcommand)
