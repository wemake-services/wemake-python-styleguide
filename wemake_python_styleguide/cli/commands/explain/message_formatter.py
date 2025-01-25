"""Provides tools for formatting explanations."""

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


def _get_whitespace_prefix(line: str) -> int | float:
    """Get length of whitespace prefix of string."""
    for char_index, char in enumerate(line):
        if char != ' ':
            return char_index
    return float('+inf')


def _get_greatest_common_indent(text: str) -> int:
    """Get the greatest common whitespace prefix length of all lines."""
    lines = text.split('\n')
    greatest_common_indent = float('+inf')
    for line in lines:
        greatest_common_indent = min(
            greatest_common_indent, _get_whitespace_prefix(line)
        )
    if isinstance(greatest_common_indent, float):
        greatest_common_indent = 0
    return greatest_common_indent


def _remove_indentation(text: str, tab_size: int = 4) -> str:
    """Remove excessive indentation."""
    text = _replace_tabs(_clean_text(text), tab_size)
    max_indent = _get_greatest_common_indent(text)
    return '\n'.join(line[max_indent:] for line in text.split('\n'))


def _remove_newlines_at_ends(text: str) -> str:
    """Remove leading and trailing newlines."""
    return text.strip('\n\r')


def format_violation(violation: ViolationInfo) -> str:
    """Format violation information."""
    cleaned_docstring = _remove_newlines_at_ends(
        _remove_indentation(violation.docstring)
    )
    violation_url = SHORTLINK_TEMPLATE.format(f'WPS{violation.code}')
    return f'{cleaned_docstring}\n\nSee at website: {violation_url}'
