# -*- coding: utf-8 -*-

from wemake_python_styleguide.violations.consistency import (
    ComparisonOrderViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class WrongOrderVisitor(BaseNodeVisitor):
    """Restricts comparision expressions where argument doesn't come first (only for single variable)."""

    def _get_num_variables(self, comparators: list) -> int:
        count = 0
        for comparator in comparators:
            if isinstance(comparator, ast.Name):
                count+=1

        return count
    
    def _check_order(self, node: ast.Compare) -> None:
        if isinstance(node.left, ast.Name):
            return
        if self._get_num_variables(node.comparators) > 1:
            return
        if isinstance(node.comparators[-1], ast.Name) != True:
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
