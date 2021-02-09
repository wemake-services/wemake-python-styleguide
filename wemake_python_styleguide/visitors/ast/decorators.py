import ast

from typing_extensions import Final, final

from wemake_python_styleguide.logic.tree import attributes
from wemake_python_styleguide.types import AnyFunctionDef
from wemake_python_styleguide.violations.best_practices import (
    NewStyledDecoratorViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

_ALLOWED_DECORATOR_TYPES: Final = (
    ast.Attribute,
    ast.Call,
    ast.Name,
)


@final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class WrongDecoratorVisitor(BaseNodeVisitor):
    """Checks decorators's correctness."""

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """Checks functions' decorators."""
        self._check_new_decorator_syntax(node)
        self.generic_visit(node)

    def _check_new_decorator_syntax(self, node: AnyFunctionDef) -> None:
        for decorator in node.decorator_list:
            if not self._is_allowed_decorator(decorator):  # pragma: py-lt-39
                self.add_violation(NewStyledDecoratorViolation(decorator))

    def _is_allowed_decorator(self, node: ast.expr) -> bool:
        if not isinstance(node, _ALLOWED_DECORATOR_TYPES):  # pragma: py-lt-39
            return False

        if isinstance(node, ast.Name):
            return True  # Simple names are fine!

        return all(
            isinstance(part, _ALLOWED_DECORATOR_TYPES)
            for part in attributes.parts(node)
        )
