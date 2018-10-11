# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, Sequence

from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations.consistency import (
    ComparisonOrderViolation,
    ConstantComparisonViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class ConstantComparisonVisitor(BaseNodeVisitor):
    """Restricts the comparison of literals."""

    def _check_is_literal(self, node: ast.AST) -> bool:
        """
        Checks for nodes that contains only constants.

        If the node contains only literals it will be evaluted.
        When node relies on some other names, it won't be evaluted.
        """
        try:
            ast.literal_eval(node)
        except ValueError:
            return False
        else:
            return True

    def _check_literal_compare(self, node: ast.Compare) -> None:
        last_was_literal = self._check_is_literal(node.left)
        for comparator in node.comparators:
            next_is_literal = self._check_is_literal(comparator)
            if last_was_literal and next_is_literal:
                self.add_violation(ConstantComparisonViolation(node))
                break
            last_was_literal = next_is_literal

    def visit_Compare(self, node: ast.Compare) -> None:
        """
        Ensures that compares are written correctly.

        Raises:
            ConstantComparisonViolation

        """
        self._check_literal_compare(node)
        self.generic_visit(node)


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

    def _has_wrong_nodes_on_the_right(
        self,
        comparators: Sequence[ast.AST],
    ) -> bool:
        for right in comparators:
            if isinstance(right, self._allowed_left_nodes):
                return True
            if isinstance(right, ast.BinOp):
                return self._has_wrong_nodes_on_the_right([
                    right.left, right.right,
                ])
        return False

    def _check_ordering(self, node: ast.Compare) -> None:
        if self._is_left_node_valid(node.left):
            return

        if self._is_special_case(node):
            return

        if len(node.comparators) > 1:
            return

        if not self._has_wrong_nodes_on_the_right(node.comparators):
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


class RedundantComparisonVisitor(BaseNodeVisitor):
    """Restricts the comparison where always same result"""

    def visit_Compare(self, node: ast.Compare) -> None:
        """
        Ensures that compares are not evaluating statement that outputs same result.

        Raises:
            ConstantComparisonViolation

        """

    def _check_redundant_compare(self, node: ast.Compare) -> None:
        last_was_variable = self._check_is_variable(node.left)
        for right in node.comparators:
            next_is_variable = self._check_is_variable(right)
            if last_was_variable and next_is_variable:
                if node.left.id is right.id:
                    self.add_violation(ConstantComparisonViolation(node))
                    break
            last_was_variable = next_is_variable
            
        self._check_redundant_compare(node)
        self.generic_visit(node)

