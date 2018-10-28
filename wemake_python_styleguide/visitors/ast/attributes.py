# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, FrozenSet

from wemake_python_styleguide.logics.naming import access
from wemake_python_styleguide.types import final
from wemake_python_styleguide.violations.best_practices import (
    ProtectedAttributeViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class WrongAttributeVisitor(BaseNodeVisitor):
    """Ensures that attributes are used correctly."""

    _allowed_to_use_protected: ClassVar[FrozenSet[str]] = frozenset((
        'self',
        'cls',
        'mcs',
    ))

    def _is_super_called(self, node: ast.Call) -> bool:
        if isinstance(node.func, ast.Name):
            if node.func.id == 'super':
                return True
        return False

    def _check_protected_attribute(self, node: ast.Attribute) -> None:
        if access.is_protected(node.attr):
            if isinstance(node.value, ast.Name):
                if node.value.id in self._allowed_to_use_protected:
                    return

            if isinstance(node.value, ast.Call):
                if self._is_super_called(node.value):
                    return

            self.add_violation(
                ProtectedAttributeViolation(node, text=node.attr),
            )

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """
        Checks the `Attribute` node.

        Raises:
            ProtectedAttributeViolation

        """
        self._check_protected_attribute(node)
        self.generic_visit(node)
