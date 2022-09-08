import ast
import math

from typing_extensions import final

from wemake_python_styleguide.compat.aliases import FunctionNodes
from wemake_python_styleguide.types import AnyFunctionDef
from wemake_python_styleguide.violations import best_practices
from wemake_python_styleguide.visitors import base
from wemake_python_styleguide.visitors.decorators import alias


@final
@alias('visit_any_function', (
    'visit_FunctionDef',
    'visit_AsyncFunctionDef',
))
class WrongEmptyLinesCountVisitor(base.BaseNodeVisitor):
    """Restricts empty lines in function or method body."""

    def visit_any_function(self, node: AnyFunctionDef) -> None:
        """Find empty lines count."""
        for subnode in ast.walk(node):
            if not isinstance(subnode, FunctionNodes):
                continue
            line_numbers_with_expressions = [
                expression.lineno for expression in subnode.body
            ]
            lines_range = set(range(
                line_numbers_with_expressions[0],
                line_numbers_with_expressions[-1] + 1,
            ))
            empty_lines_count = len(
                lines_range - set(line_numbers_with_expressions),
            )
            available_empty_lines = self._available_empty_lines(
                len(line_numbers_with_expressions),
            )
            if not empty_lines_count:
                continue
            if empty_lines_count >= available_empty_lines:
                self.add_violation(
                    best_practices.WrongEmptyLinesCountVisitorViolation(
                        node,
                        text=str(empty_lines_count),
                        baseline=available_empty_lines,
                    ),
                )

    def _available_empty_lines(self, lines_with_expressions_count: int) -> int:
        option = self.options.available_expressions_for_one_empty_line
        return math.floor(lines_with_expressions_count / option)
