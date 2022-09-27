"""
Module to define fix type differences in different python versions.

Note that we use ``sys.version_info`` directly,
because that's how ``mypy`` knows about what we are doing.
"""

import ast
import sys
from typing import Any, Optional

if sys.version_info >= (3, 8):  # pragma: py-lt-38
    from ast import Constant as Constant
    from ast import NamedExpr as NamedExpr
else:  # pragma: py-gte-38
    class NamedExpr(ast.expr):
        """
        Fallback for python that does not have ``ast.NamedExpr``.

        Copied from ast.pyi file.
        """

        value: ast.expr  # noqa: WPS110
        target: ast.expr

    class Constant(ast.expr):
        """
        Fallback for python that does not have ``ast.Constant``.

        In this case ``Constant`` is replaced with:

        - ``ast.Num``
        - ``ast.Str`` and ``ast.Bytes``
        - ``ast.NameConstant``

        Only ``python3.8+`` has this node.

        Copied from ast.pyi file.
        """

        value: Any  # noqa: WPS110
        kind: Optional[str]

        s: Any  # noqa: WPS111
        n: complex  # noqa: WPS111

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
