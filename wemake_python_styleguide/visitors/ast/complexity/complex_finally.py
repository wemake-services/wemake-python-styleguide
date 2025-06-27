import ast
from typing import final

from wemake_python_styleguide.violations import complexity
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class ComplexFinallyBlocksVisitor(BaseNodeVisitor):
    """Ensures there are no complex ``finally`` blocks."""

    def visit_Try(self, node: ast.Try) -> None:
        """Visits all finally nodes in the tree."""
        self._check_complex_finally(node)
        self.generic_visit(node)

    def _check_complex_finally(self, node: ast.Try) -> None:
        """Checks complexity of finally blocks."""
        if not node.finalbody:
            return

        first_line = node.finalbody[0].lineno
        # `end_lineno` was added in 3.8, but typing is not really correct,
        # we are pretty sure that it always exist in modern python versions.
        last_line = getattr(node.finalbody[-1], 'end_lineno', 0) or 0
        total_lines = last_line - first_line + 1
        if total_lines > self.options.max_lines_in_finally:
            self.add_violation(
                complexity.ComplexFinallyViolation(
                    node,
                    text=str(total_lines),
                    baseline=self.options.max_lines_in_finally,
                ),
            )
