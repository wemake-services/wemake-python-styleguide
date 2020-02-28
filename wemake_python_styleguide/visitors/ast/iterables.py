import ast

from typing_extensions import Final, final

from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.violations.consistency import (
    IterableUnpackingViolation,
)
from wemake_python_styleguide.visitors import base

UNPACKABLE_ITERABLE_PARENT_TYPES: Final = (ast.List, ast.Set, ast.Tuple)


@final
class IterableUnpackingVisitor(base.BaseNodeVisitor):
    """Checks iterables unpacking."""

    def visit_Starred(self, node: ast.Starred) -> None:
        """
        Checks iterable's unpacking.

        Raises:
            IterableUnpackingViolation

        """
        self._check_unneccessary_iterable_unpacking(node)
        self.generic_visit(node)

    def _check_unneccessary_iterable_unpacking(self, node: ast.Starred) -> None:
        parent = get_parent(node)
        if isinstance(parent, UNPACKABLE_ITERABLE_PARENT_TYPES):
            if len(parent.elts) == 1:
                self.add_violation(IterableUnpackingViolation(node))
