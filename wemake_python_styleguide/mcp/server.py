"""
MCP server exposing ``wemake-python-styleguide`` as tools for LLMs.

Tools
-----

``lint``
    Lint Python source code and return violations with locations,
    source context, and full rule explanations in JSON.

``lint_file``
    Lint a Python file by path on disk.

``explain_rule``
    Return the full documentation for a specific WPS violation rule.

"""

from __future__ import annotations

import json
import textwrap

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from wemake_python_styleguide.cli.commands.explain.violation_loader import (
    get_violation,
)
from wemake_python_styleguide.constants import SHORTLINK_TEMPLATE
from wemake_python_styleguide.mcp.flake8_runner import (
    lint_file as _lint_file,
    run_flake8,
)
from wemake_python_styleguide.version import pkg_version

_READ_ONLY = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=False,
)

mcp_server = FastMCP(
    'wemake-python-styleguide',
    version=pkg_version,
    instructions=textwrap.dedent("""\
        This server exposes the wemake-python-styleguide linter
        (the strictest Python linter) as tools for LLMs.

        Use "lint" to check Python source code for violations.
        Use "lint_file" to check a file on disk.
        Use "explain_rule" to get full documentation for a WPS rule.

        All tools return JSON.  Violations include the error location,
        the offending source line, and a detailed rule explanation.
    """),
)


@mcp_server.tool(
    annotations=_READ_ONLY,
    description=(
        'Lint Python source code using wemake-python-styleguide. '
        'Returns violations with locations, source context, '
        'and full rule explanations in JSON format.'
    ),
)
def lint(
    source_code: str,
    config_path: str | None = None,
    filename: str | None = None,
) -> str:
    """Lint Python source code.

    Args:
        source_code: The Python source code to lint.
        config_path: Optional absolute path to a flake8
            configuration file (setup.cfg, .flake8, etc.).
            When omitted, runs in isolated mode
            with only WPS rules enabled.
        filename: Optional display filename used for
            module-level checks (e.g. module naming rules).

    Returns:
        A JSON object with ``violations`` (array) and
        ``total_violations`` (int).
        Each violation contains ``code``, ``message``,
        ``line``, ``column``, ``source_line``,
        and for WPS rules: ``explanation`` and ``link``.

    """
    lint_result = run_flake8(
        source_code,
        config_path=config_path,
        filename=filename,
    )
    return json.dumps(lint_result, indent=2)


@mcp_server.tool(
    annotations=_READ_ONLY,
    description=(
        'Lint a Python file on disk using wemake-python-styleguide. '
        'Returns violations with locations, source context, '
        'and full rule explanations in JSON format.'
    ),
)
def lint_file(
    file_path: str,
    config_path: str | None = None,
) -> str:
    """Lint a Python file on disk.

    Args:
        file_path: Absolute path to the Python file to lint.
        config_path: Optional absolute path to a flake8
            configuration file (setup.cfg, .flake8, etc.).
            When omitted, runs in isolated mode
            with only WPS rules enabled.

    Returns:
        A JSON object with ``file``, ``violations`` (array),
        and ``total_violations`` (int).
        Each violation contains ``code``, ``message``,
        ``line``, ``column``, ``source_line``,
        and for WPS rules: ``explanation`` and ``link``.

    """
    lint_result = _lint_file(
        file_path,
        config_path=config_path,
    )
    return json.dumps(lint_result, indent=2)


@mcp_server.tool(
    annotations=_READ_ONLY,
    description=(
        'Get the full documentation for a specific WPS violation rule. '
        'Accepts codes like "WPS100" or just "100".'
    ),
)
def explain_rule(violation_code: str) -> str:
    """Explain a WPS violation rule.

    Args:
        violation_code: The WPS violation code to explain.
            Accepts full codes like ``WPS100``
            or just the numeric part like ``100``.

    Returns:
        A JSON object with ``code``, ``name``, ``section``,
        ``explanation``, and ``link``.

    """
    code_str = violation_code.removeprefix('WPS')
    try:
        code_num = int(code_str)
    except ValueError:
        return json.dumps({
            'error': f'Invalid violation code: {violation_code!r}',
        })

    violation_info = get_violation(code_num)
    if violation_info is None:
        return json.dumps({
            'error': f'Violation {violation_code!r} not found',
        })

    full_code = f'WPS{str(code_num).zfill(3)}'
    return json.dumps({
        'code': full_code,
        'name': violation_info.identifier,
        'section': violation_info.section,
        'explanation': violation_info.docstring,
        'link': SHORTLINK_TEMPLATE.format(full_code),
    })


def main() -> None:
    """Run the MCP server (stdio transport)."""
    mcp_server.run()
