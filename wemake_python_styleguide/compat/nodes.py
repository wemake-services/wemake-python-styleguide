"""
Module to define fix type differences in different python versions.

Note that we use ``sys.version_info`` directly,
because that's how ``mypy`` knows about what we are doing.
"""

import ast
import sys

if sys.version_info >= (3, 11):  # pragma: >=3.11 cover
    from ast import TryStar as TryStar
else:  # pragma: <3.11 cover

    class TryStar(ast.stmt):
        """Used for `try/except*` statements."""

        body: list[ast.stmt]
        handlers: list[ast.ExceptHandler]
        orelse: list[ast.stmt]
        finalbody: list[ast.stmt]


if sys.version_info >= (3, 12):  # pragma: # pragma: >=3.12 cover
    from ast import TypeAlias as TypeAlias
else:  # pragma: <3.12 cover

    class TypeAlias(ast.stmt):
        """Used to define `TypeAlias` nodes in `python3.12+`."""

        name: ast.Name
        type_params: list[ast.stmt]
