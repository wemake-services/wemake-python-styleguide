# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, Mapping, Optional, Tuple, Type, Union

from typing_extensions import final

from wemake_python_styleguide.logic import walk
from wemake_python_styleguide.logic.operators import (
    count_unary_operator,
    unwrap_unary_node,
)
from wemake_python_styleguide.types import AnyNodes
from wemake_python_styleguide.violations import consistency
from wemake_python_styleguide.violations.best_practices import (
    ListMultiplyViolation,
)
from wemake_python_styleguide.visitors import base, decorators

_MeaninglessOperators = Mapping[complex, Tuple[Type[ast.operator], ...]]
_OperatorLimits = Mapping[Type[ast.unaryop], int]
_NumbersAndConstants = Union[ast.Num, ast.NameConstant]


@final
@decorators.alias('visit_numbers_and_constants', (
    'visit_Num',
    'visit_NameConstant',
))
class UselessOperatorsVisitor(base.BaseNodeVisitor):
    """Checks operators used in the code."""

    _limits: ClassVar[_OperatorLimits] = {
        ast.UAdd: 0,
        ast.Invert: 1,
        ast.Not: 1,
        ast.USub: 1,
    }

    _meaningless_operations: ClassVar[_MeaninglessOperators] = {
        # ast.Div is not in the list,
        # since we have a special violation for it.
        0: (ast.Mult, ast.Add, ast.Sub, ast.Pow, ast.Mod),
        # `1` and `-1` are different, `-1` is allowed.
        1: (ast.Div, ast.Mult, ast.Pow, ast.Mod),
    }

    #: Used to ignore some special cases like `1 / x`:
    _left_special_cases: ClassVar[_MeaninglessOperators] = {
        1: (ast.Div,),
    }

    def visit_numbers_and_constants(self, node: _NumbersAndConstants) -> None:
        """
        Checks numbers unnecessary operators inside the code.

        Raises:
            UselessOperatorsViolation

        """
        self._check_operator_count(node)
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        """
        Visits binary operators.

        Raises:
            ZeroDivisionViolation

        """
        self._check_zero_division(node.op, node.right)
        self._check_useless_math_operator(node.op, node.left, node.right)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        """
        Visits augmented assigns.

        Raises:
            ZeroDivisionViolation

        """
        self._check_zero_division(node.op, node.value)
        self._check_useless_math_operator(node.op, node.value)
        self.generic_visit(node)

    def _check_operator_count(self, node: _NumbersAndConstants) -> None:
        for node_type, limit in self._limits.items():
            if count_unary_operator(node, node_type) > limit:
                text = str(node.n) if isinstance(node, ast.Num) else node.value
                self.add_violation(
                    consistency.UselessOperatorsViolation(node, text=text),
                )

    def _check_zero_division(self, op: ast.operator, number: ast.AST) -> None:
        number = unwrap_unary_node(number)

        is_zero_division = (
            isinstance(op, ast.Div) and
            isinstance(number, ast.Num) and
            number.n == 0
        )
        if is_zero_division:
            self.add_violation(consistency.ZeroDivisionViolation(number))

    def _check_useless_math_operator(
        self,
        op: ast.operator,
        left: Optional[ast.AST],
        right: Optional[ast.AST] = None,
    ) -> None:
        if isinstance(left, ast.Num) and left.n in self._left_special_cases:
            if right and isinstance(op, self._left_special_cases[left.n]):
                left = None

        non_negative_numbers = self._get_non_negative_nodes(left, right)

        for number in non_negative_numbers:
            forbidden = self._meaningless_operations.get(number.n, None)
            if forbidden and isinstance(op, forbidden):
                self.add_violation(
                    consistency.MeaninglessNumberOperationViolation(number),
                )

    def _get_non_negative_nodes(
        self,
        left: Optional[ast.AST],
        right: Optional[ast.AST] = None,
    ):
        non_negative_numbers = []
        for node in filter(None, (left, right)):
            real_node = unwrap_unary_node(node)
            if not isinstance(real_node, ast.Num):
                continue

            if real_node.n not in self._meaningless_operations:
                continue

            if real_node.n == 1 and walk.is_contained(node, ast.USub):
                continue
            non_negative_numbers.append(real_node)
        return non_negative_numbers


@final
class WrongMathOperatorVisitor(base.BaseNodeVisitor):
    """Checks that there are not wrong math operations."""

    _string_nodes: ClassVar[AnyNodes] = (
        ast.Str,
        ast.Bytes,
        ast.JoinedStr,
    )

    _list_nodes: ClassVar[AnyNodes] = (
        ast.List,
        ast.ListComp,
    )

    def visit_BinOp(self, node: ast.BinOp) -> None:
        """
        Visits binary operations.

        Raises:
            DoubleMinusOpeationViolation

        """
        self._check_negation(node.op, node.right)
        self._check_list_multiply(node)
        self._check_string_concat(node.left, node.op, node.right)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        """
        Visits augmented assignes.

        Raises:
            DoubleMinusOpeationViolation

        """
        self._check_negation(node.op, node.value)
        self._check_string_concat(node.value, node.op)
        self._check_addition_assignment_on_list(
            node.target,
            node.op,
            node.value,
        )
        self.generic_visit(node)

    def _check_negation(self, op: ast.operator, right: ast.AST) -> None:
        is_double_minus = (
            isinstance(op, (ast.Add, ast.Sub)) and
            isinstance(right, ast.UnaryOp) and
            isinstance(right.op, ast.USub)
        )
        if is_double_minus:
            self.add_violation(
                consistency.OperationSignNegationViolation(right),
            )

    def _check_list_multiply(self, node: ast.BinOp) -> None:
        is_list_multiply = (
            isinstance(node.op, ast.Mult) and
            isinstance(node.left, self._list_nodes)
        )
        if is_list_multiply:
            self.add_violation(ListMultiplyViolation(node.left))

    def _check_string_concat(
        self,
        left: ast.AST,
        op: ast.operator,
        right: Optional[ast.AST] = None,
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

    def _check_addition_assignment_on_list(
        self,
        left: ast.AST,
        op: ast.operator,
        right: ast.AST,
    ):
        is_addition_assignment_on_list = (
            isinstance(op, ast.Add) and
            isinstance(right, ast.List)
        )
        if is_addition_assignment_on_list:
            self.add_violation(
                consistency.AdditionAssignmentOnListViolation(right),
            )
