"""Contains command implementation."""

from typing import final

from attrs import frozen

from wemake_python_styleguide.cli.commands.base import AbstractCommand
from wemake_python_styleguide.cli.commands.explain import (
    service,
)
from wemake_python_styleguide.cli.output import print_stderr, print_stdout


@final
@frozen
class ExplainCommandArgs:
    """Arguments for wps explain command."""

    violation_code: str


@final
class ExplainCommand(AbstractCommand[ExplainCommandArgs]):
    """Explain command impl."""

    _args_type = ExplainCommandArgs

    def _run(self, args: ExplainCommandArgs) -> int:
        """Run command."""
        try:
            message = service.explain_violation(args.violation_code)
        except service.ViolationNotFoundError:
            print_stderr(f'Violation "{args.violation_code}" not found')
            return 1
        print_stdout(message)
        return 0
