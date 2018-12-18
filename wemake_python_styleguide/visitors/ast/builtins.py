# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, Iterable, Optional

from wemake_python_styleguide import constants
from wemake_python_styleguide.types import AnyNodes, final
from wemake_python_styleguide.violations.best_practices import (
    IncorrectUnpackingViolation,
    MagicNumberViolation,
    MultipleAssignmentsViolation,
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


@final
class WrongAssignmentVisitor(BaseNodeVisitor):
    """Visits all assign nodes."""

    def _check_assign_targets(self, node: ast.Assign) -> None:
        if len(node.targets) > 1:
            self.add_violation(MultipleAssignmentsViolation(node))

    def _check_unpacking_targets(
        self,
        node: ast.AST,
        targets: Iterable[ast.AST],
    ) -> None:
        for target in targets:
            if isinstance(target, ast.Starred):
                target = target.value
            if not isinstance(target, ast.Name):
                self.add_violation(IncorrectUnpackingViolation(node))

    def visit_With(self, node: ast.With) -> None:
        """
        Checks assignments inside context managers to be correct.

        Raises:
            IncorrectUnpackingViolation

        """
        for withitem in node.items:
            if isinstance(withitem.optional_vars, ast.Tuple):
                self._check_unpacking_targets(
                    node, withitem.optional_vars.elts,
                )
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        """
        Checks assignments inside ``for`` loops to be correct.

        Raises:
            IncorrectUnpackingViolation

        """
        if isinstance(node.target, ast.Tuple):
            self._check_unpacking_targets(node, node.target.elts)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """
        Checks assignments to be correct.

        Raises:
            MultipleAssignmentsViolation
            IncorrectUnpackingViolation

        """
        self._check_assign_targets(node)
        if isinstance(node.targets[0], ast.Tuple):
            self._check_unpacking_targets(node, node.targets[0].elts)
        self.generic_visit(node)
