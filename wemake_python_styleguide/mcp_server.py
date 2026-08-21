from wemake_python_styleguide.cli.output import print_stderr

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # pragma: no cover
    print_stderr(
        "Please use `pip install 'wemake-python-styleguide[mcp]'` "
        'to use MCP feature',
    )
    raise

from wemake_python_styleguide.cli.commands.explain.service import (
    explain_violation,
)


def create_server() -> FastMCP:
    """Create an MCP server with the violation explanation tool."""
    server = FastMCP('wemake-python-styleguide')
    server.tool()(explain_violation)
    return server


def main() -> None:
    """Run the MCP server over stdio."""
    create_server().run()
