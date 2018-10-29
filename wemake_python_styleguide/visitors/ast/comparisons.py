# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, Sequence

from wemake_python_styleguide.logics.naming.name_nodes import is_same_variable
from wemake_python_styleguide.logics.nodes import is_literal
from wemake_python_styleguide.types import AnyIf, AnyNodes, final
from wemake_python_styleguide.violations.consistency import (
    ComparisonOrderViolation,
    ConstantComparisonViolation,
    MultipleInComparisonViolation,
    RedundantComparisonViolation,
    WrongConditionalViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
class ComparisonSanityVisitor(BaseNodeVisitor):
    """Restricts the comparison of literals."""

    def _has_multiple_in_comparisons(self, node: ast.Compare) -> bool:
        count = 0
        for op in node.ops:
            if isinstance(op, ast.In):
                count += 1
        return count > 1

    def _check_literal_compare(self, node: ast.Compare) -> None:
        last_was_literal = is_literal(node.left)
        for comparator in node.comparators:
            next_is_literal = is_literal(comparator)
            if last_was_literal and next_is_literal:
                self.add_violation(ConstantComparisonViolation(node))
                break
            last_was_literal = next_is_literal

    def _check_redundant_compare(self, node: ast.Compare) -> None:
        last_variable = node.left
        for next_variable in node.comparators:
            if is_same_variable(last_variable, next_variable):
                self.add_violation(RedundantComparisonViolation(node))
                break
            last_variable = next_variable

    def _check_multiple_in_comparisons(self, node: ast.Compare) -> None:
        if self._has_multiple_in_comparisons(node):
            self.add_violation(MultipleInComparisonViolation(node))

    def visit_Compare(self, node: ast.Compare) -> None:
        """
        Ensures that compares are written correctly.

        Raises:
            ConstantComparisonViolation
            MultipleInComparisonViolation
            RedundantComparisonViolation

        """
        self._check_literal_compare(node)
        self._check_redundant_compare(node)
        self._check_multiple_in_comparisons(node)
        self.generic_visit(node)


@final
class WrongComparisionOrderVisitor(BaseNodeVisitor):
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
            left_node = self._is_left_node_valid(left.left)
            right_node = self._is_left_node_valid(left.right)
            return left_node or right_node
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


@alias('visit_any_if', (
    'visit_If',
    'visit_IfExp',
))
class WrongConditionalVisitor(BaseNodeVisitor):
    """Finds wrong conditional arguments."""

    _forbidden_nodes: ClassVar[AnyNodes] = (
        ast.List,
        ast.Set,
        ast.Num,
        ast.NameConstant,
        ast.Str,
        ast.Dict,
    )

    def visit_any_if(self, node: AnyIf) -> None:
        """
        Ensures that if statements are using valid conditionals.

        Raises:
            WrongConditionalViolation

        """
        self._check_if_statement_conditional(node)
        self.generic_visit(node)

    def _check_if_statement_conditional(self, node: AnyIf) -> None:
        if isinstance(node.test, self._forbidden_nodes):
            self.add_violation(WrongConditionalViolation(node))
