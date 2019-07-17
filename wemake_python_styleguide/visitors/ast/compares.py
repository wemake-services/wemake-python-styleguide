# -*- coding: utf-8 -*-

import ast
from typing import ClassVar, List, Optional, Sequence

import astor
from typing_extensions import final

from wemake_python_styleguide.compat.aliases import AssignNodes
from wemake_python_styleguide.compat.functions import get_assign_targets
from wemake_python_styleguide.logic import (
    compares,
    functions,
    nodes,
    operators,
)
from wemake_python_styleguide.logic.naming.name_nodes import is_same_variable
from wemake_python_styleguide.types import AnyIf, AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    HeterogenousCompareViolation,
)
from wemake_python_styleguide.violations.consistency import (
    CompareOrderViolation,
    ConstantCompareViolation,
    ConstantConditionViolation,
    MultipleInCompareViolation,
    ReversedComplexCompareViolation,
    UselessCompareViolation,
)
from wemake_python_styleguide.violations.refactoring import (
    NestedTernaryViolation,
    NotOperatorWithCompareViolation,
    SimplifiableIfViolation,
    UselessLenCompareViolation,
    WrongInCompareTypeViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias


def _is_correct_len(sign: ast.cmpop, comparator: ast.AST) -> bool:
    """This is a helper function to tell what calls to ``len()`` are valid."""
    if isinstance(comparator, (ast.Num, ast.UnaryOp)):
        numeric_value = ast.literal_eval(comparator)
        if numeric_value == 0:
            return False
        if numeric_value == 1:
            return not isinstance(sign, (ast.GtE, ast.Lt))
    return True


@final
class CompareSanityVisitor(BaseNodeVisitor):
    """Restricts the incorrect compares."""

    _wrong_in_comparators: ClassVar[AnyNodes] = (
        ast.List,
        ast.ListComp,
        ast.Dict,
        ast.DictComp,
        ast.Tuple,
        ast.GeneratorExp,
    )

    def _check_literal_compare(self, node: ast.Compare) -> None:
        last_was_literal = nodes.is_literal(node.left)
        for comparator in node.comparators:
            next_is_literal = nodes.is_literal(comparator)
            if last_was_literal and next_is_literal:
                self.add_violation(ConstantCompareViolation(node))
                break
            last_was_literal = next_is_literal

    def _check_useless_compare(self, node: ast.Compare) -> None:
        last_variable = node.left
        for next_variable in node.comparators:
            if is_same_variable(last_variable, next_variable):
                self.add_violation(UselessCompareViolation(node))
                break
            last_variable = next_variable

    def _check_in_compare(self, node: ast.Compare) -> None:
        in_nodes = (ast.In, ast.NotIn)
        count = sum(1 for op in node.ops if isinstance(op, in_nodes))
        if count > 1:
            self.add_violation(MultipleInCompareViolation(node))

        for op, comp in zip(node.ops, node.comparators):
            if not isinstance(op, in_nodes):
                continue
            if not isinstance(comp, self._wrong_in_comparators):
                continue

            self.add_violation(WrongInCompareTypeViolation(comp))

    def _check_unpythonic_compare(self, node: ast.Compare) -> None:
        all_nodes = [node.left, *node.comparators]

        for index, compare in enumerate(all_nodes):
            if not isinstance(compare, ast.Call):
                continue
            if functions.given_function_called(compare, {'len'}):
                ps = index - len(all_nodes) + 1
                if not _is_correct_len(node.ops[ps], node.comparators[ps]):
                    self.add_violation(UselessLenCompareViolation(node))

    def _check_heterogenous_operators(self, node: ast.Compare) -> None:
        if len(node.ops) == 1:
            return

        prototype = compares.get_similar_operators(node.ops[0])

        for op in node.ops:
            if not isinstance(op, prototype):
                self.add_violation(HeterogenousCompareViolation(node))
                break

    def _check_reversed_complex_compare(self, node: ast.Compare) -> None:
        if len(node.ops) != 2:
            return

        is_less = all(
            isinstance(op, (ast.Gt, ast.GtE))
            for op in node.ops
        )
        if not is_less:
            return

        self.add_violation(ReversedComplexCompareViolation(node))

    def visit_Compare(self, node: ast.Compare) -> None:
        """
        Ensures that compares are written correctly.

        Raises:
            ConstantCompareViolation
            MultipleInCompareViolation
            UselessCompareViolation
            UselessLenCompareViolation
            HeterogenousCompareViolation
            ReversedComplexCompareViolation
            WrongInCompareTypeViolation

        """
        self._check_literal_compare(node)
        self._check_useless_compare(node)
        self._check_in_compare(node)
        self._check_unpythonic_compare(node)
        self._check_heterogenous_operators(node)
        self._check_reversed_complex_compare(node)
        self.generic_visit(node)


@final
class WrongComparisionOrderVisitor(BaseNodeVisitor):
    """Restricts comparision where argument doesn't come first."""

    _allowed_left_nodes: ClassVar[AnyNodes] = (
        ast.Name,
        ast.Call,
        ast.Attribute,
        ast.Subscript,
        ast.Await,
    )

    _special_cases: ClassVar[AnyNodes] = (
        ast.In,
        ast.NotIn,
    )

    def _is_special_case(self, node: ast.Compare) -> bool:
        """
        Operators ``in`` and ``not in`` are special cases.

        Why? Because it is perfectly fine to use something like:

        .. code:: python

            if 'key' in some_dict: ...

        This should not be an issue.

        When there are multiple special operators it is still a separate issue.
        """
        return isinstance(node.ops[0], self._special_cases)

    def _is_left_node_valid(self, left: ast.AST) -> bool:
        if isinstance(left, self._allowed_left_nodes):
            return True
        if isinstance(left, ast.BinOp):
            left_node = self._is_left_node_valid(left.left)
            right_node = self._is_left_node_valid(left.right)
            return left_node or right_node
        return False

    def _has_wrong_nodes_on_the_right(
        self,
        comparators: Sequence[ast.AST],
    ) -> bool:
        for right in comparators:
            if isinstance(right, self._allowed_left_nodes):
                return True
            if isinstance(right, ast.BinOp):
                return self._has_wrong_nodes_on_the_right([
                    right.left, right.right,
                ])
        return False

    def _check_ordering(self, node: ast.Compare) -> None:
        if self._is_left_node_valid(node.left):
            return

        if self._is_special_case(node):
            return

        if len(node.comparators) > 1:
            return

        if not self._has_wrong_nodes_on_the_right(node.comparators):
            return

        self.add_violation(CompareOrderViolation(node))

    def visit_Compare(self, node: ast.Compare) -> None:
        """
        Forbids comparision where argument doesn't come first.

        Raises:
            CompareOrderViolation

        """
        self._check_ordering(node)
        self.generic_visit(node)


@final
@alias('visit_any_if', (
    'visit_If',
    'visit_IfExp',
))
class WrongConditionalVisitor(BaseNodeVisitor):
    """Finds wrong conditional arguments."""

    _forbidden_nodes: ClassVar[AnyNodes] = (
        # Constants:
        ast.Num,
        ast.Str,
        ast.Bytes,
        ast.NameConstant,

        # Collections:
        ast.List,
        ast.Set,
        ast.Dict,
        ast.Tuple,
    )

    _forbidden_expression_parents: ClassVar[AnyNodes] = (
        ast.If,
        ast.BoolOp,
        ast.BinOp,
        ast.UnaryOp,
        ast.Compare,
    )

    def visit_any_if(self, node: AnyIf) -> None:
        """
        Ensures that ``if`` nodes are using valid conditionals.

        Raises:
            ConstantConditionViolation
            SimplifiableIfViolation
            NestedTernaryViolation

        """
        if isinstance(node, ast.If):
            self._check_simplifiable_if(node)
        else:
            self._check_simplifiable_ifexpr(node)
            self._check_nested_ifexpr(node)

        self._check_constant_condition(node)
        self.generic_visit(node)

    def _is_simplifiable_assign(
        self,
        node_body: List[ast.stmt],
    ) -> Optional[str]:
        wrong_length = len(node_body) != 1
        if wrong_length or not isinstance(node_body[0], AssignNodes):
            return None
        if not isinstance(node_body[0].value, ast.NameConstant):
            return None
        if node_body[0].value.value is None:
            return None

        targets = get_assign_targets(node_body[0])
        if len(targets) != 1:
            return None

        return astor.to_source(targets[0]).strip()

    def _check_constant_condition(self, node: AnyIf) -> None:
        real_node = operators.unwrap_unary_node(node.test)
        if isinstance(real_node, self._forbidden_nodes):
            self.add_violation(ConstantConditionViolation(node))

    def _check_simplifiable_if(self, node: ast.If) -> None:
        chain = getattr(node, 'wps_chain', None)
        chained = getattr(node, 'wps_chained', None)
        if chain is None and chained is None:
            body_var = self._is_simplifiable_assign(node.body)
            else_var = self._is_simplifiable_assign(node.orelse)
            if body_var and body_var == else_var:
                self.add_violation(SimplifiableIfViolation(node))

    def _check_simplifiable_ifexpr(self, node: ast.IfExp) -> None:
        conditions = set()
        if isinstance(node.body, ast.NameConstant):
            conditions.add(node.body.value)
        if isinstance(node.orelse, ast.NameConstant):
            conditions.add(node.orelse.value)

        if conditions == {True, False}:
            self.add_violation(SimplifiableIfViolation(node))

    def _check_nested_ifexpr(self, node: ast.IfExp) -> None:
        parent = nodes.get_parent(node)
        if isinstance(parent, self._forbidden_expression_parents):
            self.add_violation(NestedTernaryViolation(node))


@final
class UnaryCompareVisitor(BaseNodeVisitor):
    """Checks that unary compare operators are used correctly."""

    def _check_incorrect_not(self, node: ast.UnaryOp) -> None:
        if not isinstance(node.op, ast.Not):
            return

        if isinstance(node.operand, ast.Compare):
            self.add_violation(NotOperatorWithCompareViolation(node))

    def visit_UnaryOp(self, node: ast.UnaryOp) -> None:
        """
        Finds bad `not` usages.

        Raises:
            NotOperatorWithCompareViolation

        """
        self._check_incorrect_not(node)
        self.generic_visit(node)
