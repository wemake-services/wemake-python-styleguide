# -*- coding: utf-8 -*-

"""
Module to define fix type differences in different python versions.

Note that we use ``sys.version_info`` directly,
because that's how ``mypy`` knows about what we are doing.
"""

import ast
import sys

if sys.version_info >= (3, 8):
    from ast import NamedExpr as NamedExpr  # noqa: WPS113, WPS433
else:
    class NamedExpr(ast.expr):  # noqa: WPS440
        """Copied from ast.pyi file."""

        target: ast.expr
        value: ast.expr  # noqa: WPS110
