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
            if not self._is_allowed_decorator(decorator):
                self.add_violation(NewStyledDecoratorViolation(decorator))

    def _is_allowed_decorator(self, decorator: ast.expr) -> bool:
        if not isinstance(decorator, _ALLOWED_DECORATOR_TYPES):
            return False

        if isinstance(decorator, ast.Name):
            return True  # Simple names are fine!

        for part in attributes.parts(decorator):  # pragma: py-lt-39
            # This part of code can only be accessed by python3.9+
            # because previous versions did not allow that
            # on a parser level. Which was cool...
            if not isinstance(part, _ALLOWED_DECORATOR_TYPES):
                return False
        return True
