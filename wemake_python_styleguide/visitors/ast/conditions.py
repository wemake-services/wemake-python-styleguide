import ast
from typing import ClassVar, List, Mapping, Set, Type

from typing_extensions import TypeAlias, final

from wemake_python_styleguide.logic import source
from wemake_python_styleguide.logic.naming.duplicates import (
    duplicated_isinstance_call,
    get_duplicate_names,
)
from wemake_python_styleguide.logic.tree import ifs, operators
from wemake_python_styleguide.logic.tree.compares import CompareBounds
from wemake_python_styleguide.logic.tree.functions import given_function_called
from wemake_python_styleguide.types import AnyIf
from wemake_python_styleguide.violations import (
    best_practices,
    consistency,
    refactoring,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

_OperatorPairs: TypeAlias = Mapping[Type[ast.boolop], Type[ast.cmpop]]


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
        self.generic_visit(node)

    def _check_negated_conditions(self, node: AnyIf) -> None:
        if isinstance(node, ast.If) and not ifs.has_else(node):
            return

        if isinstance(node.test, ast.UnaryOp):
            if isinstance(node.test.op, ast.Not):
                self.add_violation(refactoring.NegatedConditionsViolation(node))
        elif isinstance(node.test, ast.Compare):
            if any(isinstance(elem, ast.NotEq) for elem in node.test.ops):
                self.add_violation(refactoring.NegatedConditionsViolation(node))

    def _check_useless_len(self, node: AnyIf) -> None:
        if isinstance(node.test, ast.Call):
            if given_function_called(node.test, {'len'}):
                self.add_violation(refactoring.UselessLenCompareViolation(node))


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
            self.add_violation(
                best_practices.SameElementsInConditionViolation(node),
            )

    def _check_isinstance_calls(self, node: ast.BoolOp) -> None:
        if not isinstance(node.op, ast.Or):
            return

        for var_name in duplicated_isinstance_call(node):
            self.add_violation(
                refactoring.UnmergedIsinstanceCallsViolation(
                    node,
                    text=var_name,
                ),
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

        for duplicate in get_duplicate_names(variables):
            self.add_violation(
                refactoring.ImplicitInConditionViolation(node, text=duplicate),
            )

    def _check_implicit_complex_compare(self, node: ast.BoolOp) -> None:
        if not isinstance(node.op, ast.And):
            return

        if not CompareBounds(node).is_valid():
            self.add_violation(
                consistency.ImplicitComplexCompareViolation(node),
            )


@final
class ChainedIsVisitor(BaseNodeVisitor):
    """Is used to find chained `is` comparisons."""

    def visit_Compare(self, node: ast.Compare) -> None:
        """Checks for chained 'is' operators in comparisons."""
        if len(node.ops) > 1:
            if all(isinstance(op, ast.Is) for op in node.ops):
                self.add_violation(refactoring.ChainedIsViolation(node))

        self.generic_visit(node)
