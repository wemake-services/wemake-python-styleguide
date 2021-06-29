import ast
from typing import ClassVar, FrozenSet, List

from typing_extensions import final

from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.violations.best_practices import (
    ProtectedAttributeViolation,
    UnspecifiedEncodingViolation,
)
from wemake_python_styleguide.violations.oop import (
    DirectMagicAttributeAccessViolation,
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

    _allowed_magic_attributes: ClassVar[FrozenSet[str]] = frozenset((
        '__class__',
        '__name__',
        '__qualname__',
        '__doc__',
        '__subclasses__',
        '__mro__',
        '__version__',
    ))

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """
        Checks the `Attribute` node.

        Raises:
            ProtectedAttributeViolation
            DirectMagicAttributeAccessViolation

        """
        self._check_protected_attribute(node)
        self._check_magic_attribute(node)
        self.generic_visit(node)

    def _is_super_called(self, node: ast.Call) -> bool:
        if isinstance(node.func, ast.Name):
            if node.func.id == 'super':
                return True
        return False

    def _ensure_attribute_type(self, node: ast.Attribute, exception) -> None:
        if isinstance(node.value, ast.Name):
            if node.value.id in self._allowed_to_use_protected:
                return

        if isinstance(node.value, ast.Call):
            if self._is_super_called(node.value):
                return

        self.add_violation(exception(node, text=node.attr))

    def _check_protected_attribute(self, node: ast.Attribute) -> None:
        if access.is_protected(node.attr):
            self._ensure_attribute_type(node, ProtectedAttributeViolation)

    def _check_magic_attribute(self, node: ast.Attribute) -> None:
        if access.is_magic(node.attr):
            if node.attr not in self._allowed_magic_attributes:
                self._ensure_attribute_type(
                    node, DirectMagicAttributeAccessViolation,
                )


@final
class EncodingVisitor(BaseNodeVisitor):
    """Check if open function has the encoding parameter."""

    def __init__(self, *args, **kwargs) -> None:
        """Creates the booleans indicating encoding was found."""
        super().__init__(*args, **kwargs)
        self._encoding = False

    def visit_Call(self, node: ast.Call):
        """Visit calls and finds if it is an open function."""
        if isinstance(node.func, ast.Name) and node.func.id == 'open':
            if node.keywords:
                for keyword in node.keywords:
                    self._check_keywords(keyword)
            if node.args:
                self._check_args(node.args)

            if self._encoding is False:
                self.add_violation(UnspecifiedEncodingViolation(node))

        self.generic_visit(node)

    def _check_keywords(self, node: ast.keyword):
        """Check if there is an encoding parameter."""
        if node.arg == 'encoding':
            self._encoding = True

    def _check_args(self, node: List[ast.expr]):
        """Check if there is an encoding parameter."""
        if len(node) > 3:
            if isinstance(node[3], ast.Constant):
                self._encoding = True
