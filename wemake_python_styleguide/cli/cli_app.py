"""Main CLI utility file."""

import argparse
import sys

from wemake_python_styleguide.cli.application import Application
from wemake_python_styleguide.cli.output import BufferedStreamWriter


def _configure_arg_parser(app: Application) -> argparse.ArgumentParser:
    """Configures CLI arguments and subcommands."""
    parser = argparse.ArgumentParser(
        prog='wps',
        description='WPS command line tool'
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


def main() -> int:
    """Main function."""
    app = Application(BufferedStreamWriter(sys.stdout, sys.stderr))
    args = _configure_arg_parser(app).parse_args()
    return int(args.func(args))


if __name__ == '__main__':
    sys.exit(main())
