import ast
from typing import ClassVar, final

from wemake_python_styleguide.logic.tree import pattern_matching
from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations.refactoring import (
    ExtraMatchSubjectSyntaxViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class MatchSubjectVisitor(BaseNodeVisitor):
    """Restricts the incorrect subjects in PM."""

    _forbidden_syntax: ClassVar[AnyNodes] = (
        ast.Dict,
        ast.Set,
        ast.List,
        ast.Tuple,
    )

    def visit_Match(self, node: ast.Match) -> None:
        """Visits `Match` nodes and checks their internals."""
        self._check_extra_syntax(node.subject)
        self.generic_visit(node)

    def _check_extra_syntax(self, node: ast.expr) -> None:
        if not isinstance(node, self._forbidden_syntax):
            return
        if pattern_matching.is_constant_subject(node):
            return  # raises another violation in a different place
        if isinstance(node, ast.Tuple) and len(node.elts) > 1:
            return
        self.add_violation(ExtraMatchSubjectSyntaxViolation(node))
