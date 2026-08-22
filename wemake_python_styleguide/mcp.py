try:
    from mcp.server import MCPServer
except ImportError:  # pragma: no cover
    print(  # noqa: WPS421
        'Cannot import `mcp` tool, you might need to run '
        "`pip install 'wemake-python-styleguide[mcp]' to get it",
    )
    raise

from wemake_python_styleguide.cli.commands.explain.service import (
    explain_violation,
)

mcp = MCPServer('wemake-python-styleguide')
mcp.tool()(explain_violation)
