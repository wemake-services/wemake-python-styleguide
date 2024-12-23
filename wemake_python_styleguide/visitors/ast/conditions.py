import ast
from collections import Counter
from collections.abc import Mapping
from typing import ClassVar, TypeAlias

from typing_extensions import final

from wemake_python_styleguide.logic import source
from wemake_python_styleguide.logic.naming.duplicates import (
    get_duplicate_names,
)
from wemake_python_styleguide.logic.tree import (
    attributes,
    compares,
    ifs,
    operators,
)
from wemake_python_styleguide.logic.tree.functions import given_function_called
from wemake_python_styleguide.types import AnyIf, AnyNodes
from wemake_python_styleguide.violations import (
    best_practices,
    consistency,
    refactoring,
)
from wemake_python_styleguide.visitors.base import BaseNodeVisitor
from wemake_python_styleguide.visitors.decorators import alias

_OperatorPairs: TypeAlias = Mapping[type[ast.boolop], type[ast.cmpop]]


@final
@alias(
    'visit_any_if',
    (
        'visit_If',
        'visit_IfExp',
    ),
)
class IfStatementVisitor(BaseNodeVisitor):
    """Checks single and consecutive ``if`` statement nodes."""

    _nodes_to_check: ClassVar[AnyNodes] = (
        ast.Name,
        ast.Attribute,
        ast.Subscript,
        ast.Constant,
        ast.List,
        ast.Dict,
        ast.Tuple,
        ast.Set,
    )

    def __init__(self, *args, **kwargs) -> None:
        """Save visited ``if`` nodes."""
        super().__init__(*args, **kwargs)
        self._finder = ifs.NegatedIfConditions()

    def visit_any_if(self, node: AnyIf) -> None:
        """Checks ``if`` nodes and expressions."""
        self._check_negated_conditions(node)
        self._check_useless_len(node)
        self._check_repeated_conditions(node)
        self._check_useless_ternary(node)
        self.generic_visit(node)

    def _check_negated_conditions(self, node: AnyIf) -> None:
        for subnode in self._finder.negated_nodes(node):
            self.add_violation(
                refactoring.NegatedConditionsViolation(subnode),
            )

    def _check_useless_len(self, node: AnyIf) -> None:
        if isinstance(node.test, ast.Call) and given_function_called(
            node.test,
            {'len'},
        ):
            self.add_violation(refactoring.UselessLenCompareViolation(node))

    def _check_repeated_conditions(self, node: AnyIf) -> None:
        if not isinstance(node, ast.If):
            return

        conditions = [
            source.node_to_string(chained.test)
            for chained in ifs.chain(node)
            if isinstance(chained, ast.If)
        ]
        for condition, times in Counter(conditions).items():
            if times > 1:
                self.add_violation(
                    refactoring.DuplicateIfConditionViolation(
                        node,
                        text=condition,
                    )
                )

    def _check_useless_ternary(self, node: AnyIf) -> None:
        if not isinstance(node, ast.IfExp):
            return

        comp = node.test
        if not isinstance(comp, ast.Compare) or len(comp.ops) > 1:
            return  # We only check for compares with exactly one op

        if not attributes.only_consists_of_parts(
            node.body,
            self._nodes_to_check,
        ) or not attributes.only_consists_of_parts(
            node.orelse,
            self._nodes_to_check,
        ):
            return  # Only simple nodes are allowed on left and right parts

        if compares.is_useless_ternary(
            node,
            comp.ops[0],
            comp.left,
            comp.comparators[0],
        ):
            self.add_violation(refactoring.UselessTernaryViolation(node))


@final
class BooleanConditionVisitor(BaseNodeVisitor):
    """Ensures that boolean conditions are correct."""

    def __init__(self, *args, **kwargs) -> None:
        """We need to store some bool nodes not to visit them twice."""
        super().__init__(*args, **kwargs)
        self._same_nodes: list[ast.BoolOp] = []

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        """Checks that ``and`` and ``or`` conditions are correct."""
        self._check_same_elements(node)
        self.generic_visit(node)

    def _get_all_names(
        self,
        node: ast.BoolOp,
    ) -> list[str]:
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
        variables: list[set[str]] = []

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

        if not compares.CompareBounds(node).is_valid():
            self.add_violation(
                consistency.ImplicitComplexCompareViolation(node),
            )


@final
class ChainedIsVisitor(BaseNodeVisitor):
    """Is used to find chained `is` comparisons."""

    def visit_Compare(self, node: ast.Compare) -> None:
        """Checks for chained 'is' operators in comparisons."""
        if len(node.ops) > 1 and all(
            isinstance(operator, ast.Is) for operator in node.ops
        ):
            self.add_violation(refactoring.ChainedIsViolation(node))

        self.generic_visit(node)
