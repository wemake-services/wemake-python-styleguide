"""Main CLI utility file."""

import argparse
import sys
from collections.abc import Sequence

from wemake_python_styleguide.cli.application import Application
from wemake_python_styleguide.cli.output import print_stderr


def _configure_arg_parser(app: Application) -> argparse.ArgumentParser:
    """Configures CLI arguments and subcommands."""
    parser = argparse.ArgumentParser(
        prog='wps', description='WPS command line tool'
    )
    sub_parsers = parser.add_subparsers(help='sub-command help')

    parser_explain = sub_parsers.add_parser(
        'explain',
        help='Get violation description',
    )
    parser_explain.add_argument(
        'violation_code',
        help='Desired violation code',
    )
    parser_explain.set_defaults(func=app.run_explain)

    return parser


def parse_args(args: Sequence[str], app: Application) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = _configure_arg_parser(app)
    return parser.parse_args(args)


def main() -> int:
    """Main function."""
    app = Application()
    if len(sys.argv) == 1:
        print_stderr('Command not specified. Usage: wps help')
        return 1
    args = parse_args(sys.argv[1:], app)
    return int(args.func(args))


if __name__ == '__main__':
    sys.exit(main())
