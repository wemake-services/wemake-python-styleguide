import ast
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import ClassVar, TypeAlias, final

from wemake_python_styleguide.compat.aliases import TextNodes
from wemake_python_styleguide.logic import walk
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.logic.tree.operators import (
    count_unary_operator,
    get_reduced_unary_operators,
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
_UnaryOperatorsChain: TypeAlias = Sequence[type[ast.unaryop]]


@final
@decorators.alias(
    'visit_numbers_and_constants',
    (
        'visit_Num',
        'visit_NameConstant',
    ),
)
class UselessOperatorsVisitor(base.BaseNodeVisitor):  # noqa: WPS214
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
        self._check_useless_symmetric_operator(node.op, node.left, node.right)
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        """Visit boolean operators."""
        self._check_useless_bool_op_constants(node.op, node.values)
        self._check_useless_bool_op_names(node.op, node.values)
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

    def _check_useless_bool_op_constants(
        self,
        op: ast.boolop,
        nodes: list[ast.expr],
    ) -> None:
        for position, node in enumerate(nodes, 1):
            unwrapped = unwrap_unary_node(node)

            # `and` containing at least one constant
            # `or` containing bool or everything after non-bool constant
            has_useless_constant = isinstance(unwrapped, ast.Constant) and (
                isinstance(op, ast.And)
                or isinstance(unwrapped.value, bool)
                or position < len(nodes)
            )
            if has_useless_constant:
                self.add_violation(
                    consistency.MeaninglessBooleanOperationViolation(node)
                )
                return

    def _check_useless_bool_op_names(
        self,
        op: ast.boolop,
        nodes: list[ast.expr],
    ) -> None:
        unary_chains: dict[str, set[_UnaryOperatorsChain]] = defaultdict(set)
        for node in nodes:
            unwrapped = unwrap_unary_node(node)

            # `and`/`or` operators containing a duplicate name
            # with identical unary operations
            has_useless_name = False
            if isinstance(unwrapped, ast.Name):
                opchain = tuple(get_reduced_unary_operators(unwrapped))
                has_useless_name = opchain in unary_chains[unwrapped.id]
                unary_chains[unwrapped.id].add(opchain)

            if has_useless_name:
                self.add_violation(
                    consistency.MeaninglessBooleanOperationViolation(node)
                )
                return

    def _check_useless_math_operator(
        self,
        op: ast.operator,
        left: ast.AST | None,
        right: ast.AST | None = None,
    ) -> None:
        if (
            right
            and isinstance(left, ast.Constant)  # noqa: WPS222
            and left.value in self._left_special_cases
            and isinstance(op, self._left_special_cases[left.value])  # type: ignore[index]
        ):
            left = None

        non_negative_numbers = self._get_non_negative_nodes(left, right)

        for number in non_negative_numbers:
            forbidden = self._meaningless_operations.get(number.value)  # type: ignore[arg-type]
            if forbidden and isinstance(op, forbidden):
                self.add_violation(
                    consistency.MeaninglessNumberOperationViolation(number),
                )

    def _check_useless_symmetric_operator(
        self,
        op: ast.operator,
        left: ast.AST,
        right: ast.AST,
    ) -> None:
        real_left = unwrap_unary_node(left)
        real_right = unwrap_unary_node(right)
        if not (
            isinstance(real_left, ast.Constant)
            and isinstance(real_right, ast.Constant)
        ):
            return

        left_unary_ops = get_reduced_unary_operators(real_left)
        right_unary_ops = get_reduced_unary_operators(real_right)
        if isinstance(op, (ast.BitAnd, ast.BitOr, ast.BitXor)):
            is_identical_constants = (
                real_left.value == real_right.value
                and left_unary_ops == right_unary_ops
            )
            if is_identical_constants:
                self.add_violation(
                    consistency.MeaninglessNumberOperationViolation(right)
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

    _comprehensions: ClassVar[AnyNodes] = (
        ast.ListComp,
        ast.SetComp,
        ast.DictComp,
        ast.GeneratorExp,
    )

    def visit_NamedExpr(
        self,
        node: ast.NamedExpr,
    ) -> None:
        """Disallows walrus ``:=`` operator in most cases."""
        self._check_walrus_parent(node)
        self.generic_visit(node)

    def _check_walrus_parent(
        self,
        node: ast.NamedExpr,
    ) -> None:
        is_comprehension = walk.get_closest_parent(node, self._comprehensions)
        if is_comprehension:
            return

        parent = get_parent(node)
        is_while_condition = (
            isinstance(parent, ast.While) and node is parent.test
        )
        if is_while_condition:
            return

        self.add_violation(consistency.WalrusViolation(node))
