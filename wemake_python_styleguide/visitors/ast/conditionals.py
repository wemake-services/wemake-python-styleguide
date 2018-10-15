# -*- coding: utf-8 -*-

import ast

from wemake_python_styleguide.violations.consistency import (
    NamedConstantConditionalViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


class NamedConstantConditionalVisitor(BaseNodeVisitor):
    """Restricts conditionals that use only a NameConstant."""

    def visit_If(self, node: ast.If) -> None:
        """
        Ensures that conditionals are not using NameConstants only.

        Raises:
            NamedConstantConditionalViolation

        """
        self._check_constant_boolean_conditional(node)
        self.generic_visit(node)

    def _check_constant_boolean_conditional(self, node: ast.If) -> None:
        if isinstance(node.test, ast.NameConstant):
            self.add_violation(NamedConstantConditionalViolation(node))
