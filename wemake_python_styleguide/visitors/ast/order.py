# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.violations.consistency import (
    ComparisonOrderViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class WrongOrderVisitor(BaseNodeVisitor):
    """Restricts comparisions where argument doesn't come first."""

    def _check_for_in_op(self, operators: list) -> bool:
        for operator in operators:
            if isinstance(operator, ast.In):
                return True
            if isinstance(operator, ast.NotIn):
                return True

        return False

    def _get_num_variables(self, comparators: list) -> int:
        count = 0
        for comparator in comparators:
            if isinstance(comparator, ast.Name):
                count += 1

        return count

    def _check_order(self, node: ast.Compare) -> None:
        if isinstance(node.left, ast.Name):
            return
        if self._get_num_variables(node.comparators) > 1:
            return
        if self._check_for_in_op(node.ops):
            return
        if not isinstance(node.comparators[-1], ast.Name):
            return

        self.add_violation(ComparisonOrderViolation(node))

    def visit_Compare(self, node: ast.Compare) -> None:
        """
        Forbids comparisions where argument doesn't come first.

        Raises:
            ComparisonOrderViolation

        """
        self._check_order(node)
        self.generic_visit(node)
