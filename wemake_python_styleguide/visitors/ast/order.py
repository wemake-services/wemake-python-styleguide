# -*- coding: utf-8 -*-

import ast
from typing import ClassVar

from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations.consistency import (
    ComparisonOrderViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


# TODO: move to comparisons.py
class WrongOrderVisitor(BaseNodeVisitor):
    """Restricts comparision where argument doesn't come first."""

    _allowed_left_nodes: ClassVar[AnyNodes] = (
        ast.Name,
        ast.Call,
        ast.Attribute,
    )

    _special_cases: ClassVar[AnyNodes] = (
        ast.In,
        ast.NotIn,
    )

    def _is_special_case(self, node: ast.Compare) -> bool:
        """
        Operators ``in`` and ``not in`` are special cases.

        Why? Because it is perfectly fine to use something like:
        ``if 'key' in some_dict: ...``
        This should not be an issue.

        When there are multiple special operators it is still a separate issue.
        """
        return isinstance(node.ops[0], self._special_cases)

    def _is_left_node_valid(self, left: ast.AST) -> bool:
        if isinstance(left, self._allowed_left_nodes):
            return True
        if isinstance(left, ast.BinOp):
            return (
                self._is_left_node_valid(left.left) or
                self._is_left_node_valid(left.right)
            )
        return False

    def _check_ordering(self, node: ast.Compare) -> None:
        if self._is_left_node_valid(node.left):
            return

        if self._is_special_case(node):
            return

        if len(node.comparators) > 1:
            return

        self.add_violation(ComparisonOrderViolation(node))

    def visit_Compare(self, node: ast.Compare) -> None:
        """
        Forbids comparision where argument doesn't come first.

        Raises:
            ComparisonOrderViolation

        """
        self._check_ordering(node)
        self.generic_visit(node)
