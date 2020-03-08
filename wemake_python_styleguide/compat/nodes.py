"""
Module to define fix type differences in different python versions.

Note that we use ``sys.version_info`` directly,
because that's how ``mypy`` knows about what we are doing.
"""

import ast
import sys
from typing import Any, Optional

if sys.version_info >= (3, 8):  # pragma: py-lt-38
    from ast import NamedExpr as NamedExpr  # noqa: WPS113, WPS433
    from ast import Constant as Constant  # noqa: WPS433, WPS113
else:  # pragma: py-gte-38
    class NamedExpr(ast.expr):  # noqa: WPS440
        """
        Fallback for python that does not have ``ast.NamedExpr``.

        Copied from ast.pyi file.
        """

        value: ast.expr  # noqa: WPS110
        target: ast.expr

    class Constant(ast.expr):  # noqa: WPS440
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
