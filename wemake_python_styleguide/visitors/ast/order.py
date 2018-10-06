# -*- coding: utf-8 -*-

from wemake_python_styleguide.violations.consistency import (
    ComparisonOrderViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class WrongOrderVisitor(BaseNodeVisitor):
    """Restricts comparision expressions where argument doesn't come first (only for single variable)."""

    def _check_order(self, node: ast.Compare) -> None:
        if isinstance(node.left, ast.Name):
            return
        if len(node.ops) > 1:
            return
        if isinstance(node.comparators[0], ast.Compare):
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
