"""Provides tools for formatting explanations."""

import textwrap

from wemake_python_styleguide.cli.commands.explain.violation_loader import (
    ViolationInfo,
)
from wemake_python_styleguide.constants import SHORTLINK_TEMPLATE


def _remove_newlines_at_ends(text: str) -> str:
    """Remove leading and trailing newlines."""
    return text.strip('\n\r')


def format_violation(violation: ViolationInfo) -> str:
    """Format violation information."""
    cleaned_docstring = _remove_newlines_at_ends(
        textwrap.dedent(violation.docstring)
    )
    violation_url = SHORTLINK_TEMPLATE.format(f'WPS{violation.code}')
    return f'{cleaned_docstring}\n\nSee at website: {violation_url}'
