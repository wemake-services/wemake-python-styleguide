# -*- coding: utf-8 -*-

import ast
from typing import Optional

from wemake_python_styleguide.constants import MAGIC_NUMBERS_WHITELIST
from wemake_python_styleguide.errors.best_practices import MagicNumberViolation
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class MagicNumberVisitor(BaseNodeVisitor):
    """Checks magic numbers used in the code."""

    _ALLOWED_PARENTS = (
        ast.Assign,

        # Constructor usages:
        ast.FunctionDef,
        ast.arguments,

        # Primitives:
        ast.List,
        ast.Dict,
        ast.Set,
        ast.Tuple,
    )

    _PROXY_PARENTS = (
        ast.UnaryOp,
    )

    def _get_real_parent(self, node: Optional[ast.AST]) -> Optional[ast.AST]:
        """
        Returns real number's parent.

        What can go wrong?

        1. Number can be negative: ``x = -1``,
          so ``1`` has ``UnaryOp`` as parent, but should return ``Assign``

        """
        parent = getattr(node, 'parent', None)
        if isinstance(parent, self._PROXY_PARENTS):
            return self._get_real_parent(parent)
        return parent

    def _check_is_magic(self, node: ast.Num) -> None:
        parent = self._get_real_parent(node)
        if isinstance(parent, self._ALLOWED_PARENTS):
            return

        if node.n in MAGIC_NUMBERS_WHITELIST:
            return

        if isinstance(node.n, int) and node.n <= 10:
            return

        self.add_violation(MagicNumberViolation(node, text=str(node.n)))

    def visit_Num(self, node: ast.Num) -> None:
        """
        Checks numbers not to be magic constants inside the code.

        Raises:
            MagicNumberViolation

        """
        self._check_is_magic(node)
        self.generic_visit(node)
