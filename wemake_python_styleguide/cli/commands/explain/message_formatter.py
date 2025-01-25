"""Provides tools for formatting explanations."""
import textwrap

from wemake_python_styleguide.cli.commands.explain.violation_loader import (
    ViolationInfo,
)
from wemake_python_styleguide.constants import SHORTLINK_TEMPLATE


def _clean_text(text: str) -> str:
    """Normalize line endings and clean text."""
    return text.replace('\r\n', '\n').replace('\r', '\n')


def _replace_tabs(text: str, tab_size: int = 4) -> str:
    """Replace all tabs with defined amount of spaces."""
    return text.replace('\t', ' ' * tab_size)


def _remove_indentation(text: str, tab_size: int = 4) -> str:
    """Remove excessive indentation."""
    return textwrap.dedent(_replace_tabs(_clean_text(text), tab_size))


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
