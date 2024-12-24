import ast
from typing import final

from wemake_python_styleguide.violations import complexity
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class MatchSubjectsVisitor(BaseNodeVisitor):
    """Finds excessive match subjects in `match` statements."""

    def visit_Match(self, node: ast.Match) -> None:
        """Finds all `match` statements and checks their subjects."""
        self._check_match_subjects_count(node)
        self.generic_visit(node)

    def _check_match_subjects_count(self, node: ast.Match) -> None:
        if not isinstance(node.subject, ast.Tuple):
            return
        if len(node.subject.elts) <= self.options.max_match_subjects:
            return
        self.add_violation(
            complexity.TooManyMatchSubjectsViolation(
                node,
                text=str(len(node.subject.elts)),
                baseline=self.options.max_match_subjects,
            )
        )
