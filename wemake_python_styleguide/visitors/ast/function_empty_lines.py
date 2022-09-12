import ast
import math
from contextlib import suppress
from copy import copy

from typing_extensions import final

from wemake_python_styleguide import types
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

    def visit_any_function(self, node: types.AnyFunctionDef) -> None:
        """Find empty lines count."""
        start_line = node.lineno
        if not start_line or not node.end_lineno:
            return
        lines_range = set(range(start_line, node.end_lineno))
        lines_without_expressions = self._lines_without_expressions(
            copy(lines_range), node,
        )
        empty_lines_count = len(lines_without_expressions)
        available_empty_lines = self._available_empty_lines(
            len(lines_range - lines_without_expressions),
        )
        if not empty_lines_count:
            return
        if empty_lines_count > available_empty_lines:
            self.add_violation(
                best_practices.WrongEmptyLinesCountViolation(
                    node,
                    text=str(empty_lines_count),
                    baseline=available_empty_lines,
                ),
            )
        self.generic_visit(node)

    def _lines_without_expressions(
        self,
        lines_range: set[int],
        node,
    ) -> set[int]:
        for subnode in ast.walk(node):
            if isinstance(subnode, ast.Constant) and subnode.end_lineno:
                lines_range = lines_range - set(range(
                    subnode.lineno, subnode.end_lineno + 1,
                ))
            with suppress(AttributeError, KeyError):
                lines_range.remove(subnode.lineno)
        return lines_range

    def _available_empty_lines(self, lines_with_expressions_count: int) -> int:
        option = self.options.exps_for_one_empty_line
        if option == 0:
            return 0
        return math.floor(lines_with_expressions_count / option)
