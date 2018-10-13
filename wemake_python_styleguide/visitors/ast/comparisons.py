# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, Sequence

from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations.consistency import (
    ComparisonOrderViolation,
    ConstantComparisonViolation,
    MultipleInComparisonViolation,
    RedundantComparisonViolation,
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


# TODO(@sobolevn): refactor to be a single visitor
class MultipleInVisitor(BaseNodeVisitor):
    """Restricts comparision where multiple `in`s are used."""

    def _has_multiple_in_comparisons(self, node: ast.Compare) -> bool:
        count = 0
        for op in node.ops:
            if isinstance(op, ast.In):
                count += 1
        return count > 1

    def _count_in_comparisons(self, node: ast.Compare) -> None:
        if self._has_multiple_in_comparisons(node):
            self.add_violation(MultipleInComparisonViolation(node))

    def visit_Compare(self, node: ast.Compare) -> None:
        """
        Forbids comparisons including multiple 'in's in a statement.

        Raise:
            MultipleInComparisonViolation

        """
        self._count_in_comparisons(node)
        self.generic_visit(node)


class RedundantComparisonVisitor(BaseNodeVisitor):
    """Restricts the comparison where always same result."""

    def visit_Compare(self, node: ast.Compare) -> None:
        """
        Ensures that compares are not for same variable.

        Raises:
            RedundantComparisonViolation

        """
        self._check_redundant_compare(node)
        self.generic_visit(node)

    def _is_same_variable(self, left: ast.AST, right: ast.AST) -> bool:
        if isinstance(left, ast.Name) and isinstance(right, ast.Name):
            if left.id is right.id:
                return True
        return False

    def _check_redundant_compare(self, node: ast.Compare) -> None:
        last_variable = node.left
        for next_variable in node.comparators:
            if self._is_same_variable(last_variable, next_variable):
                self.add_violation(RedundantComparisonViolation(node))
                break
            last_variable = next_variable
