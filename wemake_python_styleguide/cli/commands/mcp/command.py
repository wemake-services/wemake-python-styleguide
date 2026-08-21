from typing import final

from attrs import frozen

from wemake_python_styleguide.cli.commands.base import AbstractCommand


@final
@frozen
class McpCommandArgs:
    """Arguments for wps mcp command."""


@final
class McpCommand(AbstractCommand[McpCommandArgs]):
    """MCP command implementation."""

    _args_type = McpCommandArgs

    def _run(self, args: McpCommandArgs) -> int:
        """Run the MCP server."""
        from wemake_python_styleguide import mcp_server  # noqa: PLC0415

        mcp_server.main()
        return 0
