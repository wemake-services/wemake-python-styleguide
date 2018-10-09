# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.violations.consistency import (
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
