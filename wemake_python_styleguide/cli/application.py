"""Provides WPS CLI application class."""

from typing import final

from wemake_python_styleguide.cli.commands.explain.command import ExplainCommand


@final
class Application:
    """WPS CLI application class."""

    def run_explain(self, args) -> int:
        """Run explain command."""
        return ExplainCommand().run(args)
