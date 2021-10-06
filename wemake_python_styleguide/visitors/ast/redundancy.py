import ast
from typing import Union

from typing_extensions import final

from wemake_python_styleguide.violations.best_practices import (
    RedundantEnumerateViolation,
)
from wemake_python_styleguide.visitors import base


@final
class RedundantEnumerateVisitor(base.BaseNodeVisitor):
    """Responsible for detecting redundant usages of ``enumerate`` function."""

    def visit_For(self, node: ast.For) -> None:
        """Used to find redundant usages of ``enumerate`` function."""
        self._check_for_redundant_enumerate(node)
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        """Used to find redundant usages of ``enumerate`` in async context."""
        self._check_for_redundant_enumerate(node)
        self.generic_visit(node)

    def _check_for_redundant_enumerate(self, node: Union[ast.For, ast.AsyncFor]) -> None:  # noqa: E501
        if not isinstance(node.iter, ast.Call):
            return

        if not isinstance(node.iter.func, ast.Name):
            return

        if node.iter.func.id != 'enumerate':
            return

        if isinstance(node.target, ast.Tuple):
            index_receiver = node.target.elts[0]
        else:
            index_receiver = node.target

        if isinstance(index_receiver, ast.Name) and index_receiver.id == '_':
            self.add_violation(RedundantEnumerateViolation(node))
