from mcp.server import MCPServer

from wemake_python_styleguide.cli.commands.explain.service import (
    explain_violation,
)

mcp = MCPServer('wemake-python-styleguide')
mcp.tool()(explain_violation)
