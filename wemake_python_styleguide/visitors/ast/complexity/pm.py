import ast
from typing_extensions import final

from wemake_python_styleguide.violations import complexity
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


@final
@alias(
    'visit_match',
    ('visit_Match',)
)
class MatchSubjectsVisitor(BaseNodeVisitor):
    """Finds excessive match subjects in `match` statements."""

    def visit_match(self, node: ast.Match) -> None:
        """Finds all `match` statements and checks their subjects."""
        self._check_match_subjects_count(node)
        self.generic_visit(node)

    def _check_match_subjects_count(self, node: ast.Match) -> None:
        match_subjects = getattr(node, 'subjects', [])
        if len(match_subjects) > self.options.max_match_subjects:
            self.add_violation(
                complexity.TooManyMatchSubjectsViolation(
                    node,
                    text=str(len(match_subjects)),
                    baseline=self.options.max_match_subjects,
                )
            )
