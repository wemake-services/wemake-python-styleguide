import ast
import contextlib
from typing import ClassVar, FrozenSet, List

from typing_extensions import final

from wemake_python_styleguide.constants import ALL_MAGIC_METHODS
from wemake_python_styleguide.logic.naming import access
from wemake_python_styleguide.violations.best_practices import (
    ProtectedAttributeViolation,
)
from wemake_python_styleguide.violations.oop import (
    DirectMagicAttributeAccessViolation,
)
from wemake_python_styleguide.visitors import decorators
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
@decorators.alias('visit_any_function', (
    'visit_AsyncFunctionDef',
    'visit_FunctionDef',
))
class WrongAttributeVisitor(BaseNodeVisitor):
    """Ensures that attributes are used correctly."""

    _allowed_to_use_protected: ClassVar[FrozenSet[str]] = frozenset((
        'self',
        'cls',
        'mcs',
    ))

    _func_stack: List[str] = []

    def visit_any_function(self, node: ast.FunctionDef) -> None:
        """
        Maintain a stack of function names for 'magic method' check context.

        To check for the enclosing function name further down the line,
        we maintain a stack of them to take possibility of multiple nested
        definitions into account.
        """
        with self._memorize_function_name(node.name):
            self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """Checks the `Attribute` node."""
        self._check_protected_attribute(node)
        self._check_magic_attribute(node)
        self.generic_visit(node)

    def _is_super_called(self, node: ast.Call) -> bool:
        return isinstance(node.func, ast.Name) and node.func.id == 'super'

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
            # If "magic" method being called has the same name as
            # the enclosing function, then it is a "wrapper" and thus
            # a "false positive".
            if self._func_stack:
                if node.attr == self._func_stack[-1]:
                    return

            if node.attr in ALL_MAGIC_METHODS:
                self._ensure_attribute_type(
                    node, DirectMagicAttributeAccessViolation,
                )

    @contextlib.contextmanager
    def _memorize_function_name(self, name):
        """Used to sidestep `generic_visit(node)` call requirement."""
        self._func_stack.append(name)
        yield
        self._func_stack.pop()
