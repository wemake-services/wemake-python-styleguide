import ast
from typing import ClassVar

from typing_extensions import final

from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations.consistency import (
    IterableUnpackingViolation,
)
from wemake_python_styleguide.visitors import base


@final
class IterableUnpackingVisitor(base.BaseNodeVisitor):
    """Checks iterables unpacking."""

    _upackable_iterable_parent_types: ClassVar[AnyNodes] = (
        ast.List,
        ast.Set,
        ast.Tuple,
    )

    def visit_Starred(self, node: ast.Starred) -> None:
        """
        Checks iterable's unpacking.

        Raises:
            IterableUnpackingViolation

        """
        self._check_unnecessary_iterable_unpacking(node)
        self.generic_visit(node)

    def _check_unnecessary_iterable_unpacking(self, node: ast.Starred) -> None:
        parent = get_parent(node)
        if isinstance(parent, self._upackable_iterable_parent_types):
            if len(getattr(parent, 'elts', [])) == 1:
                self.add_violation(IterableUnpackingViolation(node))
