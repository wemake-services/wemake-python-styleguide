import ast
import types
from collections.abc import Mapping
from typing import Final, TypeAlias

from wemake_python_styleguide.logic import source

#: Type to represent multiple simple operators.
_MultipleCompareOperators: TypeAlias = tuple[type[ast.cmpop], ...]

#: Type to represent `_SIMILAR_OPERATORS` constant.
_ComparesMapping: TypeAlias = Mapping[
    type[ast.cmpop],
    _MultipleCompareOperators,
]

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
