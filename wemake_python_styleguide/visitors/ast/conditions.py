import ast
from collections import defaultdict
from functools import reduce
from typing import ClassVar, DefaultDict, List, Mapping, Set, Type

from typing_extensions import Final, TypeAlias, final

from wemake_python_styleguide.compat.aliases import ForNodes
from wemake_python_styleguide.logic import source, walk
from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.logic.tree import ifs, keywords, operators
from wemake_python_styleguide.logic.tree.compares import CompareBounds
from wemake_python_styleguide.logic.tree.functions import given_function_called
from wemake_python_styleguide.types import AnyIf, AnyLoop, AnyNodes
from wemake_python_styleguide.violations.best_practices import (
    SameElementsInConditionViolation,
)
from wemake_python_styleguide.violations.consistency import (
    ImplicitComplexCompareViolation,
    MultilineConditionsViolation,
)
from wemake_python_styleguide.violations.refactoring import (
    ChainedIsViolation,
    ImplicitInConditionViolation,
    NegatedConditionsViolation,
    SimplifiableReturningIfViolation,
    UnmergedIsinstanceCallsViolation,
    UselessLenCompareViolation,
    UselessReturningElseViolation,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

_OperatorPairs: TypeAlias = Mapping[Type[ast.boolop], Type[ast.cmpop]]
_ELSE_NODES: Final = (*ForNodes, ast.While, ast.Try)


# TODO: move to logic
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


# TODO: move to logic
def _get_duplicate_names(variables: List[Set[str]]) -> Set[str]:
    return reduce(
        lambda acc, element: acc.intersection(element),
        variables,
    )


@final
@alias('visit_any_if', (
    'visit_If',
    'visit_IfExp',
))
class IfStatementVisitor(BaseNodeVisitor):
    """Checks single and consecutive ``if`` statement nodes."""

    def visit_any_if(self, node: AnyIf) -> None:
        """Checks ``if`` nodes and expressions."""
        self._check_negated_conditions(node)
        self._check_useless_len(node)
        if isinstance(node, ast.If):
            self._check_multiline_conditions(node)
            self._check_simplifiable_returning_if(node)
        self.generic_visit(node)

    def _check_negated_conditions(self, node: AnyIf) -> None:
        if isinstance(node, ast.If) and not ifs.has_else(node):
            return

        if isinstance(node.test, ast.UnaryOp):
            if isinstance(node.test.op, ast.Not):
                self.add_violation(NegatedConditionsViolation(node))
        elif isinstance(node.test, ast.Compare):
            if any(isinstance(elem, ast.NotEq) for elem in node.test.ops):
                self.add_violation(NegatedConditionsViolation(node))

    def _check_useless_len(self, node: AnyIf) -> None:
        if isinstance(node.test, ast.Call):
            if given_function_called(node.test, {'len'}):
                self.add_violation(UselessLenCompareViolation(node))

    def _check_multiline_conditions(self, node: ast.If) -> None:
        """Checks multiline conditions ``if`` statement nodes."""
        start_lineno = getattr(node, 'lineno', None)
        for sub_nodes in ast.walk(node.test):
            sub_lineno = getattr(sub_nodes, 'lineno', None)
            if sub_lineno is not None and sub_lineno > start_lineno:
                self.add_violation(MultilineConditionsViolation(node))
                break

    def _check_simplifiable_returning_if(self, node: ast.If) -> None:
        body = node.body
        simple_if_and_root = not (ifs.has_elif(node) or ifs.is_elif(node))
        if keywords.is_simple_return(body) and simple_if_and_root:
            if ifs.has_else(node):
                else_body = node.orelse
                if keywords.is_simple_return(else_body):
                    self.add_violation(SimplifiableReturningIfViolation(node))
                return

            self._check_simplifiable_returning_parent(node)

    def _check_simplifiable_returning_parent(self, node: ast.If) -> None:
        parent = get_parent(node)
        if isinstance(parent, _ELSE_NODES):
            body = parent.body + parent.orelse
        else:
            body = getattr(parent, 'body', [node])

        next_index_in_parent = body.index(node) + 1
        if keywords.next_node_returns_bool(body, next_index_in_parent):
            self.add_violation(SimplifiableReturningIfViolation(node))


@final
@alias('visit_any_loop', (
    'visit_For',
    'visit_AsyncFor',
    'visit_While',
))
class UselessElseVisitor(BaseNodeVisitor):
    """Ensures that ``else`` is used correctly for different nodes."""

    #: Nodes that break or return the execution flow.
    _returning_nodes: ClassVar[AnyNodes] = (
        ast.Break,
        ast.Raise,
        ast.Return,
        ast.Continue,
    )

    def __init__(self, *args, **kwargs) -> None:
        """We need to store visited ``if`` not to duplicate violations."""
        super().__init__(*args, **kwargs)
        self._visited_ifs: Set[ast.If] = set()

    def visit_If(self, node: ast.If) -> None:
        """Checks ``if`` statements."""
        self._check_useless_if_else(node)
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> None:
        """Checks exception handling."""
        self._check_useless_try_else(node)
        self.generic_visit(node)

    def visit_any_loop(self, node: AnyLoop) -> None:
        """Checks any loops."""
        self._check_useless_loop_else(node)
        self.generic_visit(node)

    def _check_useless_if_else(self, node: ast.If) -> None:
        real_ifs = []
        for chained_if in ifs.chain(node):
            if isinstance(chained_if, ast.If):
                if chained_if in self._visited_ifs:
                    return

                self._visited_ifs.update({chained_if})
                real_ifs.append(chained_if)
                continue

            previous_has_returns = all(
                ifs.has_nodes(self._returning_nodes, real_if.body)
                for real_if in real_ifs
            )
            current_has_returns = ifs.has_nodes(
                self._returning_nodes, chained_if,
            )

            if previous_has_returns and current_has_returns:
                self.add_violation(
                    UselessReturningElseViolation(chained_if[0]),
                )

    def _check_useless_try_else(self, node: ast.Try) -> None:
        if not node.orelse or node.finalbody:
            # `finally` cancels this rule.
            # Because refactoring `try` with `else` and `finally`
            # by moving `else` body after `finally` will change
            # the execution order.
            return

        all_except_returning = all(
            walk.is_contained(except_, self._returning_nodes)
            for except_ in node.handlers
        )
        else_returning = any(
            walk.is_contained(sub, self._returning_nodes)
            for sub in node.orelse
        )
        if all_except_returning and else_returning:
            self.add_violation(UselessReturningElseViolation(node))

    def _check_useless_loop_else(self, node: AnyLoop) -> None:
        if not node.orelse:
            return
        # An else statement makes sense if we
        # want to execute something after breaking
        # out of the loop without writing more code
        has_break = any(
            walk.is_contained(sub, ast.Break)
            for sub in node.body
        )
        if has_break:
            return
        body_returning = any(
            walk.is_contained(sub, self._returning_nodes[1:])
            for sub in node.body
        )
        else_returning = any(
            walk.is_contained(sub, self._returning_nodes)
            for sub in node.orelse
        )
        if body_returning and else_returning:
            self.add_violation(UselessReturningElseViolation(node))


@final
class BooleanConditionVisitor(BaseNodeVisitor):
    """Ensures that boolean conditions are correct."""

    def __init__(self, *args, **kwargs) -> None:
        """We need to store some bool nodes not to visit them twice."""
        super().__init__(*args, **kwargs)
        self._same_nodes: List[ast.BoolOp] = []
        self._isinstance_calls: List[ast.BoolOp] = []

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        """Checks that ``and`` and ``or`` conditions are correct."""
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

    _allowed: ClassVar[_OperatorPairs] = {
        ast.And: ast.NotEq,
        ast.Or: ast.Eq,
    }

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        """Checks ``and`` and ``or`` don't form implicit anti-patterns."""
        self._check_implicit_in(node)
        self._check_implicit_complex_compare(node)
        self.generic_visit(node)

    def _check_implicit_in(self, node: ast.BoolOp) -> None:
        variables: List[Set[str]] = []

        for cmp in node.values:
            if not isinstance(cmp, ast.Compare) or len(cmp.ops) != 1:
                return
            if not isinstance(cmp.ops[0], self._allowed[node.op.__class__]):
                return

            variables.append({source.node_to_string(cmp.left)})

        for duplicate in _get_duplicate_names(variables):
            self.add_violation(
                ImplicitInConditionViolation(node, text=duplicate),
            )

    def _check_implicit_complex_compare(self, node: ast.BoolOp) -> None:
        if not isinstance(node.op, ast.And):
            return

        if not CompareBounds(node).is_valid():
            self.add_violation(ImplicitComplexCompareViolation(node))


@final
class ChainedIsVisitor(BaseNodeVisitor):
    """Is used to find chained `is` comparisons."""

    def visit_Compare(self, node: ast.Compare) -> None:
        """Checks for chained 'is' operators in comparisons."""
        if len(node.ops) > 1:
            if all(isinstance(op, ast.Is) for op in node.ops):
                self.add_violation(ChainedIsViolation(node))

        self.generic_visit(node)
