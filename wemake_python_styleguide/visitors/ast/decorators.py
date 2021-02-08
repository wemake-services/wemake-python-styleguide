import ast
from typing import ClassVar

from typing_extensions import final

from wemake_python_styleguide.logic.tree import attributes
from wemake_python_styleguide.types import AnyFunctionDef, AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    NewStyledDecoratorViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class WrongDecoratorVisitor(BaseNodeVisitor):
    """Checks decorators's correctness."""

    _allowed_decorator_types: ClassVar[AnyNodes] = (
        ast.Attribute,
        ast.Call,
        ast.Name,
    )

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """Checks functions' decorators."""
        self._check_new_decorator_syntax(node)
        self.generic_visit(node)

    def _check_new_decorator_syntax(self, node: AnyFunctionDef) -> None:
        for decorator in node.decorator_list:
            for part in attributes.parts(decorator):  # pragma: py-lt-39
                # This part of code can only be accessed by python3.9+
                # because previous versions did not allow that
                # on a parser level. Which was cool...
                if not isinstance(part, self._allowed_decorator_types):
                    self.add_violation(NewStyledDecoratorViolation(decorator))
