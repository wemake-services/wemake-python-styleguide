from wemake_python_styleguide.cli.commands.base import AbstractCommand
from wemake_python_styleguide.cli.commands.explain import (
    message_formatter,
    violation_loader,
)


def _format_violation_code(violation_str: str) -> int:
    if violation_str.startswith("WPS"):
        violation_str = violation_str[3:]
    return int(violation_str)


class ExplainCommand(AbstractCommand):
    def run(self, args):
        code = _format_violation_code(args.violation_code)
        violation = violation_loader.get_violation(code)
        if violation is None:
            self.writer.write_err("Violation not found")
            return 1
        message = message_formatter.format_violation(violation)
        self.writer.write_out(message)
