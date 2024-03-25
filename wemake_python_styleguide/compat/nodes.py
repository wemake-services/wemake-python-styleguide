"""
Module to define fix type differences in different python versions.

Note that we use ``sys.version_info`` directly,
because that's how ``mypy`` knows about what we are doing.
"""

import ast
import sys
from typing import Optional

if sys.version_info >= (3, 10):  # pragma: py-lt-310
    from ast import Match as Match
    from ast import MatchAs as MatchAs
    from ast import match_case as match_case
else:  # pragma: py-gte-310
    class Match(ast.stmt):
        """Used for ``match`` keyword and its body."""

    class match_case(ast.AST):  # noqa: N801
        """Used as a top level wrapper of pattern matched cases."""

    class MatchAs(ast.AST):
        """Used to declare variables in pattern matched code."""

        name: Optional[str]  # noqa: WPS110
        pattern: Optional[ast.AST]

if sys.version_info >= (3, 11):  # pragma: py-lt-311
    from ast import TryStar as TryStar
else:  # pragma: py-gte-311
    class TryStar(ast.stmt):
        """Used for `try/except*` statements."""

        body: list[ast.stmt]
        handlers: list[ast.ExceptHandler]
        orelse: list[ast.stmt]
        finalbody: list[ast.stmt]
