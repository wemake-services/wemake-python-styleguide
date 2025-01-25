"""Main CLI utility file."""

import argparse
import sys

from wemake_python_styleguide.cli.application import Application


def _configure_arg_parser(app: Application) -> argparse.ArgumentParser:
    """Configures CLI arguments and subcommands."""
    parser = argparse.ArgumentParser(
        prog='wps', description='WPS command line tool'
    )
    sub_parsers = parser.add_subparsers(help='sub-command help')
    sub_parsers.required = True

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


def parse_args(app: Application) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = _configure_arg_parser(app)
    return parser.parse_args()


def main() -> int:
    """Main function."""
    app = Application()
    args = parse_args(app)
    return int(args.func(args))


if __name__ == '__main__':
    sys.exit(main())
