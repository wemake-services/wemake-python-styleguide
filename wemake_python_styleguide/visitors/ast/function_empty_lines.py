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
        empty_lines_count = 0
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
        if empty_lines_count:
            self.add_violation(
                best_practices.WrongEmptyLinesCountVisitorViolation(
                    node,
                    text=str(empty_lines_count),
                    baseline=0,
                ),
            )
