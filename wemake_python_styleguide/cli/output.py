"""Provides tool for outputting data."""

import sys


def print_stdout(*args: str) -> None:
    """Write usual text. Works as print."""
    sys.stdout.write(' '.join(args))
    sys.stdout.write('\n')
    sys.stdout.flush()


def print_stderr(*args: str) -> None:
    """Write error text. Works as print."""
    sys.stderr.write(' '.join(args))
    sys.stderr.write('\n')
    sys.stderr.flush()
