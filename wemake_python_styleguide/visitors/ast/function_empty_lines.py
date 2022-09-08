import ast

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
            if not empty_lines_count:
                continue
            if not self._proportion_allow(empty_lines_count, len(lines_range)):
                self.add_violation(
                    best_practices.WrongEmptyLinesCountVisitorViolation(
                        node,
                        text=str(empty_lines_count),
                        baseline=0,
                    ),
                )

    def _proportion_allow(
        self,
        empty_lines_count: int,
        function_body_len: int,
    ) -> bool:
        empty_lines_proportion = empty_lines_count / function_body_len
        option = self.options.available_expressions_for_one_empty_line
        if option == 0 and empty_lines_count:
            return False
        available_values = 1 / option
        return empty_lines_proportion > available_values
