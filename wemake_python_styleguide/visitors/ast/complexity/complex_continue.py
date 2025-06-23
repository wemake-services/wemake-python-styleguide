import ast
from typing import final

from wemake_python_styleguide.violations import complexity
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class ComplexFinallyBlocksVisitor(BaseNodeVisitor):
    """Ensures there are no complex ``finally`` blocks."""

    def visit_Finally(self, node: ast.Try) -> None:
        """Visits all finally nodes in the tree."""
        self._check_complex_finally(node)
        self.generic_visit(node)

    def _check_complex_finally(self, node: ast.Try) -> None:
        """Checks complexity of finally blocks."""
        if not node.finalbody:
            return

        total_lines = 0
        for statement in node.finalbody:
            if not hasattr(statement, 'lineno'):
                continue

            start_line = statement.lineno
            end_line = getattr(statement, 'end_lineno', None)

            if end_line is not None:
                total_lines += end_line - start_line + 1
            else:
                total_lines += 1

        if total_lines > self.options.max_lines_in_finally:
            self.add_violation(complexity.ComplexFinallyViolation(node))
