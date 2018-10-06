# -*- coding: utf-8 -*-

from wemake_python_styleguide.violations.consistency import (
    ComparisonOrderViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class WrongOrderVisitor(BaseNodeVisitor):
    """Restricts comparision expressions where argument doesn't come first (only for single variable)."""

    def _check_order(self, node: ast.Compare) -> None:
        left = node.left
        ops = node.ops
        comparators = node.comparators

        if isinstance(left, ast.Name):
            return
        if len(ops) > 1:
            return
        if isinstance(comparators[0], ast.Compare):
            return

        self.add_violation(ComparisonOrderViolation(node))

    def visit_Compare(self, node: ast.Compare) -> None:
        """
        Forbids comparision expressions where argument doesn't come first (only for single variable).

        Raises:
            ComparisonOrderViolation

        """
        self._check_order(node)
        self.generic_visit(node)
