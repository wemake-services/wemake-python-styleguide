import ast
from typing import Union

from typing_extensions import final

from wemake_python_styleguide.types import AnyComprehension, AnyFor
from wemake_python_styleguide.violations.best_practices import (
    RedundantEnumerateViolation,
    RedundantTernaryViolation,
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


@final
class RedundantTernaryVisitor(BaseNodeVisitor):
    """Finds useless ternary operators."""

    allowed_ops = (ast.NotEq, ast.Eq, ast.IsNot)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        """Finds useless ternary operators."""
        body = ast.unparse(node.body)
        orelse = ast.unparse(node.orelse)

        # Check for specific patterns.
        self.body_orelse_check(node, body, orelse)
        self.check_computed_equal(node)

        self.generic_visit(node)  # Visit all other node types.

    def body_orelse_check(self, node, body, orelse) -> None:
        """Check if body and orelse are the same."""
        if body == orelse:
            self.add_violation(RedundantTernaryViolation(node))

    def check_computed_equal(self, node) -> None:
        """Used to check if the computed branches are equal."""
        if not isinstance(node.test, ast.Compare):
            return

        correct_op = any(
            isinstance(node.test.ops[0], op) for op in self.allowed_ops
        )

        if correct_op and len(node.test.ops) == 1:
            left = ast.unparse(node.test.left)
            right = ast.unparse(node.test.comparators[0])

            self.compare_operands(node, left, right)

    def compare_operands(self, node, left, right) -> None:
        """Compare each operand to see if will result in same values."""
        body_str = ast.unparse(node.body)
        orelse_str = ast.unparse(node.orelse)

        if body_str == left and orelse_str == right:
            self.add_violation(RedundantTernaryViolation(node))
        elif body_str == right and orelse_str == left:
            self.add_violation(RedundantTernaryViolation(node))
