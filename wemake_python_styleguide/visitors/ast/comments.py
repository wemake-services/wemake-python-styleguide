import ast
from typing import cast, final

from wemake_python_styleguide.logic.tokens.comments import (
    count_comments_in_range,
)
from wemake_python_styleguide.types import AnyFunctionDef
from wemake_python_styleguide.violations.best_practices import (
    TooManyCommentsViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeTokenVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
@alias(
    'visit_any_function',
    (
        'visit_FunctionDef',
        'visit_AsyncFunctionDef',
    ),
)
class FunctionCommentsVisitor(BaseNodeTokenVisitor):
    """Checks comment count limits inside functions."""

    def visit_any_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> None:
        """Checks comment count for each function."""
        self._check_comments_count(node)
        self.generic_visit(node)

    def _check_comments_count(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> None:
        """Checks whether the function exceeds the max allowed comment count."""
        nested_ranges: list[tuple[int, int]] = [
            (child.lineno, cast(int, child.end_lineno))
            for child in ast.walk(node)
            if isinstance(child, AnyFunctionDef) and child is not node
        ]

        nested_ranges.sort()

        comments_count = 0
        cursor = node.lineno

        for n_start, n_end in nested_ranges:
            if cursor < n_start:
                comments_count += count_comments_in_range(
                    self.file_tokens,
                    cursor,
                    n_start - 1,
                )
            cursor = n_end + 1

        if cursor <= cast(int, node.end_lineno):
            comments_count += count_comments_in_range(
                self.file_tokens,
                cursor,
                cast(int, node.end_lineno),
            )

        if comments_count > self.options.max_comments_in_function:
            self.add_violation(
                TooManyCommentsViolation(
                    node,
                    text=str(comments_count),
                    baseline=self.options.max_comments_in_function,
                ),
            )
