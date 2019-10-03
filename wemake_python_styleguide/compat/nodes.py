# -*- coding: utf-8 -*-

import ast

try:  # pragma: no cover
    from ast import Constant as Constant  # noqa: WPS433, WPS113
except ImportError:  # pragma: no cover
    class Constant(ast.AST):  # type: ignore  # noqa: WPS440
        """
        Fallback for pythons that do not have ``ast.Constant``.

        In this case ``Constant`` is replaced with:

        - ``ast.Num``
        - ``ast.Str`` and ``ast.Bytes``
        - ``ast.NameConstant``

        Only ``python3.8+`` has this node.
        """
