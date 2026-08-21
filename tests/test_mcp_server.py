"""Tests for the optional MCP server."""

import asyncio
from unittest.mock import MagicMock

import pytest
from mcp.server.fastmcp import FastMCP

from wemake_python_styleguide import mcp_server
from wemake_python_styleguide.cli.commands.explain import (
    message_formatter,
    violation_loader,
)
from wemake_python_styleguide.cli.commands.explain.service import (
    ViolationNotFoundError,
)

_VIOLATION_CODE = 123


def test_explain_violation_matches_cli():
    """MCP explanations use the same formatter as the CLI."""
    violation = violation_loader.get_violation(_VIOLATION_CODE)
    assert violation is not None
    expected = message_formatter.format_violation(violation)

    assert mcp_server.explain_violation('WPS123') == expected


def test_explain_violation_rejects_unknown_code():
    """Unknown violation codes produce a clear tool error."""
    with pytest.raises(ViolationNotFoundError, match='UNKNOWN'):
        mcp_server.explain_violation('UNKNOWN')


def test_create_server_registers_explanation_tool():
    """The MCP server advertises the explanation tool."""
    tools = asyncio.run(mcp_server.create_server().list_tools())

    assert [tool.name for tool in tools] == ['explain_violation']


def test_main_runs_server(monkeypatch):
    """The MCP entry point starts its configured server."""
    server = MagicMock(spec=FastMCP)
    create_server_mock = MagicMock(return_value=server)
    monkeypatch.setattr(mcp_server, 'create_server', create_server_mock)

    mcp_server.main()

    server.run.assert_called_once_with()
