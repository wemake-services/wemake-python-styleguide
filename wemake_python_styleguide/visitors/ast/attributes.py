import ast

from typing_extensions import final

from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.logic.tree import attributes
from wemake_python_styleguide.violations.base import ASTViolation
from wemake_python_styleguide.violations.best_practices import (
    ProtectedAttributeViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class WrongAttributeVisitor(BaseNodeVisitor):
    """Ensures that attributes are used correctly."""

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """Checks the `Attribute` node."""
        self._check_protected_attribute(node)
        self.generic_visit(node)

    def _is_super_called(self, node: ast.Call) -> bool:
        return isinstance(node.func, ast.Name) and node.func.id == 'super'

    def _ensure_attribute_type(
        self,
        node: ast.Attribute,
        exception: type[ASTViolation],
    ) -> None:
        if attributes.is_special_attr(node):
            return

        if isinstance(node.value, ast.Call) and self._is_super_called(
            node.value,
        ):
            return

        self.add_violation(exception(node, text=node.attr))

    def _check_protected_attribute(self, node: ast.Attribute) -> None:
        if access.is_protected(node.attr):
            self._ensure_attribute_type(node, ProtectedAttributeViolation)
