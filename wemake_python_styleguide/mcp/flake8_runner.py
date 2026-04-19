"""Run ``flake8`` as a subprocess and parse structured output."""

from __future__ import annotations

import subprocess  # noqa: S404
from pathlib import Path

from wemake_python_styleguide.cli.commands.explain.violation_loader import (
    get_violation,
)
from wemake_python_styleguide.constants import SHORTLINK_TEMPLATE

#: Separator used in the custom flake8 format string.
_SEP = '|||'

#: Fields produced by the custom format string.
_FORMAT_FIELDS = (
    '%(code)s',
    '%(row)d',
    '%(col)d',
    '%(text)s',
)

#: Expected number of parts when splitting a formatted output line.
_EXPECTED_PARTS = len(_FORMAT_FIELDS)

#: Custom flake8 format string for machine-readable output.
_FORMAT = _SEP.join(_FORMAT_FIELDS)


def _get_explanation(code: str) -> str | None:
    """Look up the full docstring for a WPS violation code."""
    try:
        code_num = int(code.removeprefix('WPS'))
    except ValueError:
        return None
    violation_info = get_violation(code_num)
    if violation_info is None:
        return None
    return violation_info.docstring


def _source_at(source_lines: list[str], row: int) -> str:
    """Return the source line at the given 1-based row, or empty."""
    if 0 < row <= len(source_lines):
        return source_lines[row - 1].rstrip()
    return ''


def _enrich_wps(
    violation: dict[str, object],
    code: str,
) -> None:
    """Add explanation and link for WPS violations in-place."""
    if not code.startswith('WPS'):
        return
    explanation = _get_explanation(code)
    if explanation is not None:
        violation['explanation'] = explanation
    violation['link'] = SHORTLINK_TEMPLATE.format(code)


def _build_violation(
    parts: tuple[str, ...],
    source_lines: list[str],
) -> dict[str, object]:
    """Build a single violation dict from parsed parts."""
    code, row_str, col_str, text = parts

    violation: dict[str, object] = {
        'code': code,
        'message': text,
        'line': int(row_str),
        'column': int(col_str),
        'source_line': _source_at(source_lines, int(row_str)),
    }
    _enrich_wps(violation, code)
    return violation


def _parse_violations(
    raw_output: str,
    source_lines: list[str],
) -> list[dict[str, object]]:
    """Parse flake8 output into structured violation dicts."""
    violations: list[dict[str, object]] = []
    for line in raw_output.strip().splitlines():
        parts = line.split(_SEP, maxsplit=3)
        if len(parts) != _EXPECTED_PARTS:
            continue
        violations.append(
            _build_violation(tuple(parts), source_lines),
        )
    return violations


def run_flake8(
    source_code: str,
    config_path: str | None = None,
    filename: str | None = None,
) -> dict[str, object]:
    """
    Run ``flake8`` on the given source code string.

    Args:
        source_code: Python source code to lint.
        config_path: Optional path to a ``flake8`` configuration file.
        filename: Optional display filename for module-level checks.

    Returns:
        A dict with ``violations`` (list) and ``total_violations`` (int).

    """
    display_name = filename or 'stdin'
    cmd = [
        'flake8',
        f'--format={_FORMAT}',
        f'--stdin-display-name={display_name}',
    ]

    if config_path:
        cmd.append(f'--config={config_path}')
    else:
        cmd.extend(('--isolated', '--select=WPS'))

    cmd.append('-')  # read from stdin

    completed = subprocess.run(  # noqa: S603
        cmd,
        input=source_code,
        capture_output=True,
        text=True,
        check=False,
    )

    source_lines = source_code.splitlines()
    violations = _parse_violations(completed.stdout, source_lines)

    return {
        'violations': violations,
        'total_violations': len(violations),
    }


def lint_file(
    file_path: str,
    config_path: str | None = None,
) -> dict[str, object]:
    """
    Run ``flake8`` on a file by path.

    Args:
        file_path: Path to the Python file to lint.
        config_path: Optional path to a ``flake8`` configuration file.

    Returns:
        A dict with ``violations`` (list) and ``total_violations`` (int).

    """
    source_code = Path(file_path).read_text(encoding='utf-8')
    cmd = [
        'flake8',
        f'--format={_FORMAT}',
    ]

    if config_path:
        cmd.append(f'--config={config_path}')
    else:
        cmd.extend(('--isolated', '--select=WPS'))

    cmd.append(file_path)

    completed = subprocess.run(  # noqa: S603
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )

    source_lines = source_code.splitlines()
    violations = _parse_violations(completed.stdout, source_lines)

    return {
        'file': file_path,
        'violations': violations,
        'total_violations': len(violations),
    }
