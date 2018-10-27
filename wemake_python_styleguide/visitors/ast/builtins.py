# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, Optional

from wemake_python_styleguide import constants
from wemake_python_styleguide.types import AnyNodes, final
from wemake_python_styleguide.violations.best_practices import (
    MagicNumberViolation,
)
from wemake_python_styleguide.violations.consistency import (
    FormattedStringViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class WrongStringVisitor(BaseNodeVisitor):
    """Restricts to use ``f`` strings."""

    def visit_JoinedStr(self, node: ast.JoinedStr) -> None:
        """
        Restricts to use ``f`` strings.

        Raises:
            FormattedStringViolation

        """
        self.add_violation(FormattedStringViolation(node))
        self.generic_visit(node)


@final
class MagicNumberVisitor(BaseNodeVisitor):
    """Checks magic numbers used in the code."""

    _allowed_parents: ClassVar[AnyNodes] = (
        ast.Assign,

        # Constructor usages:
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.arguments,

        # Primitives:
        ast.List,
        ast.Dict,
        ast.Set,
        ast.Tuple,
    )

    _proxy_parents: ClassVar[AnyNodes] = (
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
        if isinstance(parent, self._proxy_parents):
            return self._get_real_parent(parent)
        return parent

    def _check_is_magic(self, node: ast.Num) -> None:
        parent = self._get_real_parent(node)
        if isinstance(parent, self._allowed_parents):
            return

        if node.n in constants.MAGIC_NUMBERS_WHITELIST:
            return

        if isinstance(node.n, int) and node.n <= constants.NON_MAGIC_MODULO:
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
