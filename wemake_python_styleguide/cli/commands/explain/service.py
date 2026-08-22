from typing import final

from typing_extensions import Self

from wemake_python_styleguide.cli.commands.explain import (
    message_formatter,
    violation_loader,
)


@final
class ViolationNotFoundError(Exception):
    """Raised when a violation code cannot be resolved."""

    @classmethod
    def from_violation_code(cls, violation_code: str) -> Self:
        """
        This exception can show up in MCP and `wps explain` logs.

        It needs a lot of context to be readable and clear.
        """
        return cls(
            f'Unknown violation code {violation_code!r}, no such rule exists',
        )


def explain_violation(violation_code: str) -> str:
    """
    Return the formatted explanation for a violation code.

    Raises:
        ViolationNotFoundError: when we can't parse the violation docs.
    """
    normalized_code = violation_code.removeprefix('WPS')
    try:
        code = int(normalized_code)
    except ValueError as exc:
        raise ViolationNotFoundError.from_violation_code(
            violation_code,
        ) from exc

    violation = violation_loader.get_violation(code)
    if violation is None:
        raise ViolationNotFoundError.from_violation_code(violation_code)
    return message_formatter.format_violation(violation)
