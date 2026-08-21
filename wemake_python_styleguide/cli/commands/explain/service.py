"""Provides the shared violation explanation service."""

from wemake_python_styleguide.cli.commands.explain import (
    message_formatter,
    violation_loader,
)


class ViolationNotFoundError(ValueError):
    """Raised when a violation code cannot be resolved."""


def explain_violation(violation_code: str) -> str:
    """Return the formatted explanation for a violation code."""
    normalized_code = violation_code.removeprefix('WPS')
    try:
        code = int(normalized_code)
    except ValueError as exc:
        raise ViolationNotFoundError(violation_code) from exc

    violation = violation_loader.get_violation(code)
    if violation is None:
        raise ViolationNotFoundError(violation_code)
    return message_formatter.format_violation(violation)
