import argparse

from wemake_python_styleguide.cli.commands.explain.command import ExplainCommand
from wemake_python_styleguide.cli.commands.mcp.command import McpCommand


def _configure_arg_parser() -> argparse.ArgumentParser:
    """Configures CLI arguments and subcommands."""
    parser = argparse.ArgumentParser(
        prog='wps',
        description='WPS command line tool',
    )
    sub_parsers = parser.add_subparsers(
        help='sub-parser for exact wps commands',
        required=True,
    )

    parser_explain = sub_parsers.add_parser(
        'explain',
        help='Get violation description',
    )
    parser_explain.add_argument(
        'violation_code',
        help='Desired violation code',
    )
    parser_explain.set_defaults(func=ExplainCommand())

    parser_mcp = sub_parsers.add_parser(
        'mcp',
        help='Run the MCP server',
    )
    parser_mcp.set_defaults(func=McpCommand())

    return parser


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = _configure_arg_parser()
    return parser.parse_args()


def main() -> int:
    """Main function."""
    args = parse_args()
    return int(args.func(args=args))
