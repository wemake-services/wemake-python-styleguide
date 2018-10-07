# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.violations.consistency import (
    ComparisonOrderViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class WrongOrderVisitor(BaseNodeVisitor):
    """Restricts comparisions where argument doesn't come first."""

    def _get_num_variables_and_calls(self, comparators: list) -> int:
        count = 0
        for comparator in comparators:
            if (isinstance(comparator, ast.Name) or
                    isinstance(comparator, ast.Call)):
                count += 1

        return count

    def _get_num_variables_and_calls_in_BinOp(self, node):
        count = 0
        if not isinstance(node, ast.BinOp):
            return 0
        if isinstance(node.left, ast.Name) or isinstance(node.left, ast.Call):
            count += 1
        if isinstance(node.right, ast.Name) or isinstance(node.right, ast.Call):
            count += 1
        if count != 0:
            return count

        return (self._get_num_variables_and_calls_in_BinOp(node.left) +
                self._get_num_variables_and_calls_in_BinOp(node.right))

    def visit_Compare(self, node: ast.Compare) -> None:
        """
        Forbids comparisions where argument doesn't come first.

        Raises:
            ComparisonOrderViolation

        """
        if isinstance(node.left, ast.Name) or isinstance(node.left, ast.Call):
            return
        if (self._get_num_variables_and_calls(node.comparators) > 1 or
                self._get_num_variables_and_calls_in_BinOp(node.left) > 0):
            return

        # Check for in op
        for operator in node.ops:
            if (isinstance(operator, ast.In) or
                    isinstance(operator, ast.NotIn)):
                return
        if (not isinstance(node.comparators[-1], ast.Name) and
                not isinstance(node.comparators[-1], ast.BinOp)):
            return

        self.add_violation(ComparisonOrderViolation(node))
        self.generic_visit(node)
