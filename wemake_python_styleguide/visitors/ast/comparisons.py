# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.violations.consistency import (
    ConstantComparisonViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class ConstantComparisonVisitor(BaseNodeVisitor):
    """Restricts the comparison of literals."""

    def _check_is_literal(self, node: ast.AST) -> bool:
        try:
            ast.literal_eval(node)
        except ValueError:
            return False
        else:
            return True

    def visit_Compare(self, node: ast.Compare) -> None:
        """
        Restricts comparisons between two literals.

        Raises:
            ConstantComparisonViolation

        """
        last_was_literal = self._check_is_literal(node.left)
        for comparator in node.comparators:
            next_is_literal = self._check_is_literal(comparator)
            if last_was_literal and next_is_literal:
                self.add_violation(ConstantComparisonViolation(node))
                break
            last_was_literal = next_is_literal
        self.generic_visit(node)
