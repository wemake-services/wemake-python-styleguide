"""Exposes violation explanations over the Model Context Protocol."""

from mcp.server.fastmcp import FastMCP

from wemake_python_styleguide.cli.commands.explain.service import (
    explain_violation as _explain_violation,
)


def explain_violation(violation_code: str) -> str:
    """Explain a wemake-python-styleguide violation such as ``WPS123``."""
    return _explain_violation(violation_code)


def create_server() -> FastMCP:
    """Create an MCP server with the violation explanation tool."""
    server = FastMCP('wemake-python-styleguide')
    server.tool()(explain_violation)
    return server


def main() -> None:
    """Run the MCP server over stdio."""
    create_server().run()
