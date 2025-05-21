import ast
from typing import Final, final

from wemake_python_styleguide.compat.constants import PY312
from wemake_python_styleguide.logic.tree import attributes
from wemake_python_styleguide.options.validation import ValidatedOptions
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

_ALLOWED_DECORATOR_TYPES3_12: Final = (
    *_ALLOWED_DECORATOR_TYPES,
    ast.Subscript,  # PEP 695 - Type Parameter Syntax
)


@final
@alias(
    'visit_any_function',
    (
        'visit_FunctionDef',
        'visit_AsyncFunctionDef',
    ),
)
class WrongDecoratorVisitor(BaseNodeVisitor):
    """Checks decorators's correctness."""

    def __init__(
        self,
        options: ValidatedOptions,
        tree: ast.AST,
        **kwargs,
    ) -> None:
        """Creates Decorator Visitor."""
        self.ALLOWED_DECORATOR_TYPES: Final = (
            _ALLOWED_DECORATOR_TYPES3_12 if PY312 else _ALLOWED_DECORATOR_TYPES
        )
        super().__init__(options, tree, **kwargs)

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """Checks functions' decorators."""
        self._check_new_decorator_syntax(node)
        self.generic_visit(node)

    def _check_new_decorator_syntax(self, node: AnyFunctionDef) -> None:
        for decorator in node.decorator_list:
            if not self._is_allowed_decorator(decorator):
                self.add_violation(NewStyledDecoratorViolation(decorator))

    def _is_allowed_decorator(self, node: ast.expr) -> bool:
        if not isinstance(node, self.ALLOWED_DECORATOR_TYPES):
            return False

        if isinstance(node, ast.Name):
            return True  # Simple names are fine!

        return attributes.only_consists_of_parts(
            node, self.ALLOWED_DECORATOR_TYPES
        )
