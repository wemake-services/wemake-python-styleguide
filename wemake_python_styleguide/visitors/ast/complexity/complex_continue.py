import ast
from typing import final

from wemake_python_styleguide.violations import complexity
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class ComplexFinallyBlocksVisitor(BaseNodeVisitor):
    """Ensures that are no complex ``continue`` blocks."""

    def visit_Finally(self, node: ast.Try) -> None:
        """Visits all finally nodes in the tree."""
        self._check_complex_finally(node)
        self.generic_visit(node)

    def _check_complex_finally(self, node: ast.Try) -> None:
        # Check complex in finally block
        finally_body = node.finalbody

        if not finally_body:
            return

        lines: set[tuple[int, int | None]] = set()

        for n in node.finalbody:  # Only traverse the module's top-level.
            if hasattr(n, 'lineno'):
                lines.add((n.lineno, n.end_lineno))

        nlines = sum(e - s + 1 for s, e in lines if e is not None)

        if nlines > self.options.max_lines_in_finally:
            self.add_violation(complexity.ComplexFinallyViolation(node))
