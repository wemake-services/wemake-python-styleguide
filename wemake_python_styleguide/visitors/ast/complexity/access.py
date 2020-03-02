import ast
from itertools import takewhile
from typing import Set, cast

from typing_extensions import final

from wemake_python_styleguide.logic.tree import attributes
from wemake_python_styleguide.types import AnyAccess
from wemake_python_styleguide.violations.complexity import (
    TooDeepAccessViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
class AccessVisitor(BaseNodeVisitor):
    """Counts access number for expressions."""

    def __init__(self, *args, **kwargs) -> None:
        """Keeps visited accesses to not visit them again."""
        super().__init__(*args, **kwargs)
        self._visited_accesses: Set[AnyAccess] = set()

    def visit_Subscript(self, node: ast.Attribute) -> None:
        """
        Checks subscript access number.

        Raises:
            TooDeepAccessViolation

        """
        self._check_consecutive_access_number(node)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Subscript) -> None:
        """
        Checks attribute access number.

        Raises:
            TooDeepAccessViolation

        """
        self._check_consecutive_access_number(node)
        self.generic_visit(node)

    def _is_any_access(self, node: ast.AST) -> bool:
        return isinstance(node, (ast.Attribute, ast.Subscript))

    def _check_consecutive_access_number(self, node: AnyAccess) -> None:
        if node in self._visited_accesses:
            return

        consecutive_access = cast(Set[AnyAccess], set(takewhile(
            self._is_any_access,
            attributes.parts(node),
        )))

        self._visited_accesses.update(consecutive_access)
        access_number = len(consecutive_access)

        if access_number > self.options.max_access_level:
            self.add_violation(
                TooDeepAccessViolation(
                    node,
                    text=str(access_number),
                    baseline=self.options.max_access_level,
                ),
            )
