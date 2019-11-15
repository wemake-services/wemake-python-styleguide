# -*- coding: utf-8 -*-

import ast
from collections import defaultdict
from functools import reduce
from typing import ClassVar, DefaultDict, Dict, List, Set, Type

from typing_extensions import final

from wemake_python_styleguide.logic import ifs, operators, source
from wemake_python_styleguide.logic.compares import CompareBounds
from wemake_python_styleguide.logic.functions import given_function_called
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.types import AnyIf, AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    SameElementsInConditionViolation,
)
from wemake_python_styleguide.violations.consistency import (
    ImplicitComplexCompareViolation,
    ImplicitTernaryViolation,
    MultilineConditionsViolation,
)
from wemake_python_styleguide.violations.refactoring import (
    ImplicitInConditionViolation,
    NegatedConditionsViolation,
    UnmergedIsinstanceCallsViolation,
    UselessLenCompareViolation,
    UselessReturningElseViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor


def _duplicated_isinstance_call(node: ast.BoolOp) -> List[str]:
    counter: DefaultDict[str, int] = defaultdict(int)

    for call in node.values:
        if not isinstance(call, ast.Call) or len(call.args) != 2:
            continue

        if not given_function_called(call, {'isinstance'}):
            continue

        isinstance_object = source.node_to_string(call.args[0])
        counter[isinstance_object] += 1

    return [
        node_name
        for node_name, count in counter.items()
        if count > 1
    ]


def _get_duplicate_names(variables: List[Set[str]]):
    return reduce(
        lambda acc, element: acc.intersection(element),
        variables,
    )


@final
class IfStatementVisitor(BaseNodeVisitor):
    """Checks single and consecutive ``if`` statement nodes."""

    #: Nodes that break or return the execution flow.
    _returning_nodes: ClassVar[AnyNodes] = (
        ast.Break,
        ast.Raise,
        ast.Return,
        ast.Continue,
    )

    def __init__(self, *args, **kwargs) -> None:
        """We need to store visited ``if`` not to dublicate violations."""
        super().__init__(*args, **kwargs)
        self._visited_ifs: Set[ast.If] = set()

    def visit_If(self, node: ast.If) -> None:
        """
        Checks ``if`` nodes.

        Raises:
            UselessReturningElseViolation
            NegatedConditionsViolation
            MultilineConditionsViolation
            UselessLenCompareViolation

        """
        self._check_negated_conditions(node)
        self._check_useless_else(node)
        self._check_multiline_conditions(node)
        self._check_useless_len(node)
        self.generic_visit(node)

    def visit_IfExp(self, node: ast.IfExp) -> None:
        """
        Checks ``if`` expressions.

        Raises:
            UselessLenCompareViolation

        """
        self._check_useless_len(node)
        self.generic_visit(node)

    def _check_negated_conditions(self, node: ast.If) -> None:
        if not node.orelse:
            return

        if isinstance(node.test, ast.UnaryOp):
            if isinstance(node.test.op, ast.Not):
                self.add_violation(NegatedConditionsViolation(node))
        elif isinstance(node.test, ast.Compare):
            if any(isinstance(elem, ast.NotEq) for elem in node.test.ops):
                self.add_violation(NegatedConditionsViolation(node))

    def _check_multiline_conditions(self, node: ast.If) -> None:
        """Checks multiline conditions ``if`` statement nodes."""
        start_lineno = getattr(node, 'lineno', None)
        for sub_nodes in ast.walk(node.test):
            sub_lineno = getattr(sub_nodes, 'lineno', None)
            if sub_lineno is not None and sub_lineno > start_lineno:
                self.add_violation(MultilineConditionsViolation(node))
                break

    def _check_useless_else(self, node: ast.If) -> None:
        real_ifs = []
        for chained_if in ifs.chain(node):
            if isinstance(chained_if, ast.If):
                if chained_if in self._visited_ifs:
                    return

                self._visited_ifs.update({chained_if})
                real_ifs.append(chained_if)
                continue

            previous_has_returns = all(
                ifs.has_nodes(
                    self._returning_nodes,
                    real_if.body,
                )
                for real_if in real_ifs
            )
            current_has_returns = ifs.has_nodes(
                self._returning_nodes, chained_if,
            )

            if previous_has_returns and current_has_returns:
                self.add_violation(
                    UselessReturningElseViolation(chained_if[0]),
                )

    def _check_useless_len(self, node: AnyIf) -> None:
        if isinstance(node.test, ast.Call):
            if given_function_called(node.test, {'len'}):
                self.add_violation(UselessLenCompareViolation(node))


@final
class BooleanConditionVisitor(BaseNodeVisitor):
    """Ensures that boolean conditions are correct."""

    def __init__(self, *args, **kwargs) -> None:
        """We need to store some bool nodes not to visit them twice."""
        super().__init__(*args, **kwargs)
        self._same_nodes: List[ast.BoolOp] = []
        self._isinstance_calls: List[ast.BoolOp] = []

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        """
        Checks that ``and`` and ``or`` conditions are correct.

        Raises:
            SameElementsInConditionViolation
            UnmergedIsinstanceCallsViolation

        """
        self._check_same_elements(node)
        self._check_isinstance_calls(node)
        self.generic_visit(node)

    def _get_all_names(
        self,
        node: ast.BoolOp,
    ) -> List[str]:
        # We need to make sure that we do not visit
        # one chained `BoolOp` elements twice:
        self._same_nodes.append(node)

        names = []
        for operand in node.values:
            if isinstance(operand, ast.BoolOp):
                names.extend(self._get_all_names(operand))
            else:
                names.append(
                    source.node_to_string(
                        operators.unwrap_unary_node(operand),
                    ),
                )
        return names

    def _check_same_elements(self, node: ast.BoolOp) -> None:
        if node in self._same_nodes:
            return  # We do not visit nested `BoolOp`s twice.

        operands = self._get_all_names(node)
        if len(set(operands)) != len(operands):
            self.add_violation(SameElementsInConditionViolation(node))

    def _check_isinstance_calls(self, node: ast.BoolOp) -> None:
        if not isinstance(node.op, ast.Or):
            return

        for var_name in _duplicated_isinstance_call(node):
            self.add_violation(
                UnmergedIsinstanceCallsViolation(node, text=var_name),
            )


@final
class ImplicitBoolPatternsVisitor(BaseNodeVisitor):
    """Is used to find implicit patterns that are formed by boolops."""

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        """
        Checks that ``and`` and ``or`` do not form implicit anti-patterns.

        Raises:
            ImplicitTernaryViolation
            ImplicitComplexCompareViolation
            ImplicitInConditionViolation

        """
        self._check_implicit_in(node)
        self._check_implicit_ternary(node)
        self._check_implicit_complex_compare(node)
        self.generic_visit(node)

    def _check_implicit_in(self, node: ast.BoolOp) -> None:
        allowed_ops: Dict[Type[ast.boolop], Type[ast.cmpop]] = {
            ast.And: ast.NotEq,
            ast.Or: ast.Eq,
        }

        variables: List[Set[str]] = []

        for compare in node.values:
            if not isinstance(compare, ast.Compare) or len(compare.ops) != 1:
                return

            if not isinstance(compare.ops[0], allowed_ops[node.op.__class__]):
                return

            variables.append({source.node_to_string(compare.left)})

        for duplicate in _get_duplicate_names(variables):
            self.add_violation(
                ImplicitInConditionViolation(node, text=duplicate),
            )

    def _check_implicit_ternary(self, node: ast.BoolOp) -> None:
        if isinstance(get_parent(node), ast.BoolOp):
            return

        if not isinstance(node.op, ast.Or):
            return

        if len(node.values) != 2:
            return

        if not isinstance(node.values[0], ast.BoolOp):
            return

        is_implicit_ternary = (
            len(node.values[0].values) == 2 and
            not isinstance(node.values[1], ast.BoolOp) and
            isinstance(node.values[0].op, ast.And) and
            not isinstance(node.values[0].values[1], ast.BoolOp)
        )
        if is_implicit_ternary:
            self.add_violation(ImplicitTernaryViolation(node))

    def _check_implicit_complex_compare(self, node: ast.BoolOp) -> None:
        if not isinstance(node.op, ast.And):
            return

        if not CompareBounds(node).is_valid():
            self.add_violation(ImplicitComplexCompareViolation(node))
