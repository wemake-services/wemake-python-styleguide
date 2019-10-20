# -*- coding: utf-8 -*-

import ast

from typing_extensions import final

from wemake_python_styleguide.violations import consistency
from wemake_python_styleguide.visitors import base


@final
class SubscriptVisitor(base.BaseNodeVisitor):
    """Checks subscripts used in the code."""

    def visit_Subscript(self, node: ast.Subscript) -> None:
        """
        Visits subscript.

        Raises:
            RedundantSubscriptViolation

        """
        self._check_redundant_subscript(node)
        self.generic_visit(node)

    def _check_redundant_subscript(self, node: ast.Subscript) -> None:
        if not isinstance(node.slice, ast.Slice):
            return

        lower_ok = (
            (node.slice.lower is None) or (
                not self._is_zero(node.slice.lower) and
                not self._is_none(node.slice.lower)
            )
        )

        upper_ok = (
            (node.slice.upper is None) or
            not self._is_none(node.slice.upper)
        )

        step_ok = (
            (node.slice.step is None) or (
                not self._is_one(node.slice.step) and
                not self._is_none(node.slice.step)
            )
        )

        if not (lower_ok and upper_ok and step_ok):
            self.add_violation(
                consistency.RedundantSubscriptViolation(
                    node, text=str(node),
                ),
            )

    def _is_none(self, component_value: ast.expr) -> bool:
        return (
            isinstance(component_value, ast.NameConstant) and
            component_value.value is None
        )

    def _is_zero(self, component_value: ast.expr) -> bool:
        return isinstance(component_value, ast.Num) and component_value.n == 0

    def _is_one(self, component_value: ast.expr) -> bool:
        return isinstance(component_value, ast.Num) and component_value.n == 1
