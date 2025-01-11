"""Contains command implementation."""

from wemake_python_styleguide.cli.commands.base import AbstractCommand
from wemake_python_styleguide.cli.commands.explain import (
    message_formatter,
    violation_loader,
)


def _clean_violation_code(violation_str: str) -> int:
    """
    Get int violation code from str violation code.

    Args:
        violation_str: violation code expressed as string
                       WPS412, 412 - both acceptable

    Returns:
        integer violation code

    Throws:
        ValueError: violation str is not an integer (except WPS prefix).
    """
    violation_str = violation_str.removeprefix('WPS')
    try:
        return int(violation_str)
    except ValueError:
        return -1


class ExplainCommand(AbstractCommand):
    """Explain command impl."""

    def run(self, args) -> int:
        """Run command."""
        code = _clean_violation_code(args.violation_code)
        violation = violation_loader.get_violation(code)
        if violation is None:
            self.writer.write_err('Violation not found')
            self.writer.flush()
            return 1
        message = message_formatter.format_violation(violation)
        self.writer.write_out(message)
        self.writer.flush()
        return 0
