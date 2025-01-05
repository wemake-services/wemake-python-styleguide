"""Provides WPS CLI application class."""

from wemake_python_styleguide.cli.commands.base import AbstractCommand
from wemake_python_styleguide.cli.commands.explain.command import ExplainCommand
from wemake_python_styleguide.cli.output import Writable


class Application:
    """WPS CLI application class."""

    def __init__(self, writer: Writable):
        """Create application."""
        self._writer = writer

    def run_explain(self, args) -> int:
        """Run explain command."""
        return self._get_command(ExplainCommand).run(args)

    def _get_command(
        self,
        command_class: type[AbstractCommand],
    ) -> AbstractCommand:
        """Create command from its class and inject the selected writer."""
        return command_class(writer=self._writer)
