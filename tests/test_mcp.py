import asyncio

import pytest
from mcp import Client
from mcp.server import MCPServer

from wemake_python_styleguide import mcp
from wemake_python_styleguide.cli.commands.explain import (
    message_formatter,
    violation_loader,
)
from wemake_python_styleguide.cli.commands.explain.service import (
    ViolationNotFoundError,
    explain_violation,
)

_VIOLATION_CODE = 123


async def _assert_explanation_tool_response() -> None:
    async with Client(mcp.mcp) as client:
        response = await client.call_tool(
            'explain_violation',
            {'violation_code': 'WPS123'},
        )

        assert not response.is_error
        assert response.structured_content == {
            'result': explain_violation('WPS123'),
        }


def test_explain_violation_matches_cli():
    """MCP explanations use the same formatter as the CLI."""
    violation = violation_loader.get_violation(_VIOLATION_CODE)
    assert violation is not None
    expected = message_formatter.format_violation(violation)

    assert explain_violation('WPS123') == expected


def test_explain_violation_rejects_unknown_code():
    """Unknown violation codes produce a clear tool error."""
    with pytest.raises(ViolationNotFoundError, match='UNKNOWN'):
        explain_violation('UNKNOWN')


def test_create_server_registers_explanation_tool():
    """The MCP server advertises the explanation tool."""
    tools = asyncio.run(mcp.mcp.list_tools())

    assert [tool.name for tool in tools] == ['explain_violation']


def test_server_uses_v2_sdk():
    """The MCP server uses the supported v2 server class."""
    assert isinstance(mcp.mcp, MCPServer)


def test_explanation_tool_over_mcp_protocol():
    """The registered tool can be called by an MCP v2 client."""
    asyncio.run(_assert_explanation_tool_response())
