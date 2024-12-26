import ast
from typing import ClassVar, final

from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations.consistency import (
    IterableUnpackingViolation,
)
from wemake_python_styleguide.visitors import base


@final
class IterableUnpackingVisitor(base.BaseNodeVisitor):
    """Checks iterables unpacking."""

    _unpackable_iterable_parent_types: ClassVar[AnyNodes] = (
        ast.List,
        ast.Set,
        ast.Tuple,
    )

    def visit_Starred(self, node: ast.Starred) -> None:
        """Checks iterable's unpacking."""
        self._check_unnecessary_iterable_unpacking(node)
        self.generic_visit(node)

    def _check_unnecessary_iterable_unpacking(self, node: ast.Starred) -> None:
        parent = get_parent(node)
        if not isinstance(parent, self._unpackable_iterable_parent_types):
            return
        if len(getattr(parent, 'elts', [])) != 1:
            return

        container = get_parent(parent)
        if isinstance(container, ast.Subscript):  # pragma: >=3.11 cover
            # We ignore cases like `Tuple[*Shape]`, because it is a type
            # annotation which should be used like this.
            # It is only possible for Python 3.11+
            return
        self.add_violation(IterableUnpackingViolation(node))
