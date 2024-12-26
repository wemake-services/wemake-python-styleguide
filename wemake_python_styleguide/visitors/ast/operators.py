import ast
from collections.abc import Mapping
from typing import ClassVar, TypeAlias, final

from wemake_python_styleguide.compat.aliases import TextNodes
from wemake_python_styleguide.logic import walk
from wemake_python_styleguide.logic.tree.operators import (
    count_unary_operator,
    unwrap_unary_node,
)
from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations import consistency
from wemake_python_styleguide.violations.best_practices import (
    ListMultiplyViolation,
)
from wemake_python_styleguide.visitors import base, decorators

_MeaninglessOperators: TypeAlias = Mapping[
    complex,
    tuple[type[ast.operator], ...],
]
_OperatorLimits: TypeAlias = Mapping[type[ast.unaryop], int]


@final
@decorators.alias(
    'visit_numbers_and_constants',
    (
        'visit_Num',
        'visit_NameConstant',
    ),
)
class UselessOperatorsVisitor(base.BaseNodeVisitor):
    """Checks operators used in the code."""

    _unary_limits: ClassVar[_OperatorLimits] = {
        ast.UAdd: 0,
        ast.Invert: 1,
        ast.Not: 1,
        ast.USub: 1,
    }

    _meaningless_operations: ClassVar[_MeaninglessOperators] = {
        # ast.Div and ast.Mod is not in the list,
        # since we have a special violation for it.
        0: (
            ast.Mult,
            ast.Add,
            ast.Sub,
            ast.Pow,
            ast.BitAnd,
            ast.BitOr,
            ast.BitXor,
            ast.RShift,
            ast.LShift,
        ),
        # `1` and `-1` are different, `-1` is allowed.
        1: (
            ast.Div,
            ast.FloorDiv,
            ast.Mult,
            ast.Pow,
            ast.Mod,
        ),
    }

    #: Used to ignore some special cases like `1 / x`:
    _left_special_cases: ClassVar[_MeaninglessOperators] = {
        1: (ast.Div, ast.FloorDiv),
    }

    _zero_divisors: ClassVar[AnyNodes] = (
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
    )

    def visit_numbers_and_constants(self, node: ast.Constant) -> None:
        """Checks numbers unnecessary operators inside the code."""
        self._check_operator_count(node)
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        """Visits binary operators."""
        self._check_zero_division(node.op, node.right)
        self._check_useless_math_operator(node.op, node.left, node.right)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        """Visits augmented assigns."""
        self._check_zero_division(node.op, node.value)
        self._check_useless_math_operator(node.op, node.value)
        self.generic_visit(node)

    def _check_operator_count(self, node: ast.Constant) -> None:
        for node_type, limit in self._unary_limits.items():
            if count_unary_operator(node, node_type) > limit:
                self.add_violation(
                    consistency.UselessOperatorsViolation(
                        node,
                        text=str(node.value),
                    ),
                )

    def _check_zero_division(self, op: ast.operator, number: ast.AST) -> None:
        number = unwrap_unary_node(number)

        is_zero_division = (
            isinstance(op, self._zero_divisors)
            and isinstance(number, ast.Constant)
            and number.value == 0
        )
        if is_zero_division:
            self.add_violation(consistency.ZeroDivisionViolation(number))

    def _check_useless_math_operator(
        self,
        op: ast.operator,
        left: ast.AST | None,
        right: ast.AST | None = None,
    ) -> None:
        if (
            isinstance(left, ast.Constant)
            and left.value in self._left_special_cases
            and right
            and isinstance(op, self._left_special_cases[left.value])
        ):
            left = None

        non_negative_numbers = self._get_non_negative_nodes(left, right)

        for number in non_negative_numbers:
            forbidden = self._meaningless_operations.get(number.value, None)
            if forbidden and isinstance(op, forbidden):
                self.add_violation(
                    consistency.MeaninglessNumberOperationViolation(number),
                )

    def _get_non_negative_nodes(
        self,
        left: ast.AST | None,
        right: ast.AST | None = None,
    ) -> list[ast.Constant]:
        non_negative_numbers: list[ast.Constant] = []
        for node in filter(None, (left, right)):
            real_node = unwrap_unary_node(node)
            if (
                isinstance(real_node, ast.Constant)
                and real_node.value in self._meaningless_operations
                and not (
                    real_node.value == 1 and walk.is_contained(node, ast.USub)
                )
            ):
                non_negative_numbers.append(real_node)
        return non_negative_numbers


@final
class WrongMathOperatorVisitor(base.BaseNodeVisitor):
    """Checks that there are not wrong math operations."""

    _string_nodes: ClassVar[AnyNodes] = (
        TextNodes,
        ast.JoinedStr,
    )

    _list_nodes: ClassVar[AnyNodes] = (
        ast.List,
        ast.ListComp,
    )

    def visit_BinOp(self, node: ast.BinOp) -> None:
        """Visits binary operations."""
        self._check_negation(node.op, node.right)
        self._check_list_multiply(node)
        self._check_string_concat(node.left, node.op, node.right)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        """Visits augmented assigns."""
        self._check_negation(node.op, node.value)
        self._check_string_concat(node.value, node.op)
        self.generic_visit(node)

    def _check_negation(self, op: ast.operator, right: ast.AST) -> None:
        is_double_minus = (
            isinstance(op, ast.Add | ast.Sub)
            and isinstance(right, ast.UnaryOp)
            and isinstance(right.op, ast.USub)
        )
        if is_double_minus:
            self.add_violation(
                consistency.OperationSignNegationViolation(right),
            )

    def _check_list_multiply(self, node: ast.BinOp) -> None:
        is_list_multiply = isinstance(node.op, ast.Mult) and isinstance(
            node.left,
            self._list_nodes,
        )
        if is_list_multiply:
            self.add_violation(ListMultiplyViolation(node.left))

    def _check_string_concat(
        self,
        left: ast.AST,
        op: ast.operator,
        right: ast.AST | None = None,
    ) -> None:
        if not isinstance(op, ast.Add):
            return

        left_line = getattr(left, 'lineno', 0)
        if left_line != getattr(right, 'lineno', left_line):
            # By default we treat nodes that do not have lineno
            # as nodes on the same line.
            return

        for node in (left, right):
            if isinstance(node, self._string_nodes):
                self.add_violation(
                    consistency.ExplicitStringConcatViolation(node),
                )
                return


@final
class WalrusVisitor(base.BaseNodeVisitor):
    """We use this visitor to find walrus operators and ban them."""

    _available_parents: ClassVar[AnyNodes] = (
        ast.ListComp,
        ast.SetComp,
        ast.DictComp,
        ast.GeneratorExp,
    )

    def visit_NamedExpr(
        self,
        node: ast.NamedExpr,
    ) -> None:
        """Disallows walrus ``:=`` operator outside comprehensions."""
        self._check_walrus_in_comprehesion(node)
        self.generic_visit(node)

    def _check_walrus_in_comprehesion(
        self,
        node: ast.NamedExpr,
    ) -> None:
        is_comprension = walk.get_closest_parent(node, self._available_parents)
        if is_comprension:
            return

        self.add_violation(consistency.WalrusViolation(node))
