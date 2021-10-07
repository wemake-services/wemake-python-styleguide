import ast
from typing import Union

from typing_extensions import final

from wemake_python_styleguide.types import AnyComprehension, AnyFor
from wemake_python_styleguide.violations.best_practices import (
    RedundantEnumerateViolation,
)
from wemake_python_styleguide.visitors import decorators
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


@final
@decorators.alias('visit_any_for', (
    'visit_For',
    'visit_AsyncFor',
))
@decorators.alias('visit_any_comprehension', (
    'visit_ListComp',
    'visit_DictComp',
    'visit_SetComp',
    'visit_GeneratorExp',
))
class RedundantEnumerateVisitor(BaseNodeVisitor):
    """Responsible for detecting redundant usages of ``enumerate`` function."""

    def visit_any_comprehension(self, node: AnyComprehension) -> None:
        """Finds incorrect patterns inside comprehensions."""
        for generator_node in node.generators:
            self._check_for_redundant_enumerate(generator_node)
        self.generic_visit(node)

    def visit_any_for(self, node: AnyFor) -> None:
        """Used to find redundant usages of ``enumerate`` function."""
        self._check_for_redundant_enumerate(node)
        self.generic_visit(node)

    def _check_for_redundant_enumerate(self, node: Union[AnyFor, ast.comprehension]) -> None:  # noqa: E501
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
            self.add_violation(RedundantEnumerateViolation(index_receiver))
