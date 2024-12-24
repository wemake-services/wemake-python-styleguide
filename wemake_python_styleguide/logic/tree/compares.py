import ast
import types
from collections import defaultdict
from collections.abc import Mapping
from typing import Final, TypeAlias, final

import attr

from wemake_python_styleguide.logic import source


@final
@attr.dataclass(frozen=True, slots=True)
class _Bounds:
    """Represents the bounds we use to calculate the similar compare nodes."""

    lower_bound: set[ast.Compare] = attr.ib(factory=set)
    upper_bound: set[ast.Compare] = attr.ib(factory=set)


_MultipleCompareOperators: TypeAlias = tuple[type[ast.cmpop], ...]

#: Type to represent `_SIMILAR_OPERATORS` constant.
_ComparesMapping: TypeAlias = Mapping[
    type[ast.cmpop],
    _MultipleCompareOperators,
]

#: Used to track the operator usages in `a > b and b >c` compares.
_OperatorUsages: TypeAlias = defaultdict[str, _Bounds]

#: Constant to define similar operators.
_SIMILAR_OPERATORS: Final[_ComparesMapping] = types.MappingProxyType(
    {
        ast.Gt: (ast.Gt, ast.GtE),
        ast.GtE: (ast.Gt, ast.GtE),
        ast.Lt: (ast.Lt, ast.LtE),
        ast.LtE: (ast.Lt, ast.LtE),
    },
)


def get_similar_operators(
    operator: ast.cmpop,
) -> type[ast.cmpop] | _MultipleCompareOperators:
    """Returns similar operators types for the given operator."""
    operator_type = type(operator)
    return _SIMILAR_OPERATORS.get(operator_type, operator_type)


@final
class CompareBounds:
    """
    Calculates bounds of expressions like ``a > b and b > c`` in python.

    Later we call ``.is_valid()`` method to be sure that we raise
    violations for incorrect bounds.

    Credit goes to:
    https://github.com/PyCQA/pylint/blob/master/pylint/checkers/refactoring.py
    """

    def __init__(self, node: ast.BoolOp) -> None:
        """Conctructs the basic data to calculate the bounds."""
        self._node = node
        self._uses: _OperatorUsages = defaultdict(_Bounds)

    def is_valid(self) -> bool:
        """We say that bounds are invalid, when we can refactor them."""
        local_uses = self._build_bounds().values()
        for bounds in local_uses:
            num_shared = len(
                bounds.lower_bound.intersection(bounds.upper_bound),
            )
            num_lower_bounds = len(bounds.lower_bound)
            num_upper_bounds = len(bounds.upper_bound)
            if num_shared < num_lower_bounds and num_shared < num_upper_bounds:
                return False
        return True

    def _build_bounds(self) -> _OperatorUsages:
        for comparison_node in self._node.values:
            if isinstance(comparison_node, ast.Compare):
                self._find_lower_upper_bounds(comparison_node)
        return self._uses

    def _find_lower_upper_bounds(
        self,
        comparison_node: ast.Compare,
    ) -> None:
        left_operand = comparison_node.left
        comparators = zip(
            comparison_node.ops,
            comparison_node.comparators,
            strict=False,
        )

        for operator, right_operand in comparators:
            for operand in (left_operand, right_operand):
                self._mutate(
                    comparison_node,
                    operator,
                    source.node_to_string(operand),
                    operand is left_operand,
                )
            left_operand = right_operand

    def _mutate(
        self,
        comparison_node: ast.Compare,
        operator: ast.cmpop,
        name: str,
        is_left: bool,
    ) -> None:
        key_name = None
        if isinstance(operator, ast.Lt | ast.LtE):
            key_name = 'lower_bound' if is_left else 'upper_bound'
        elif isinstance(operator, ast.Gt | ast.GtE):
            key_name = 'upper_bound' if is_left else 'lower_bound'

        if key_name:
            getattr(self._uses[name], key_name).add(comparison_node)


def is_useless_ternary(
    node: ast.IfExp,
    cmpop: ast.cmpop,
    left: ast.expr,
    right: ast.expr,
) -> bool:
    """Checks if the given ternary expression parts are useless."""
    if isinstance(cmpop, ast.Is | ast.Eq):
        comparators = {
            source.node_to_string(left),
            source.node_to_string(right),
        }
        common_elements = {
            source.node_to_string(node.body),
            source.node_to_string(node.orelse),
        }.intersection(comparators)
        return len(common_elements) == len(comparators)
    if isinstance(cmpop, ast.IsNot | ast.NotEq):
        return source.node_to_string(node.body) == source.node_to_string(
            left,
        ) and source.node_to_string(node.orelse) == source.node_to_string(
            right,
        )
    return False
