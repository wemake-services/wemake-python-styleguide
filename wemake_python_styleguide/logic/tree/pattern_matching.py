import ast
from collections.abc import Iterable

from wemake_python_styleguide.logic.nodes import get_parent
from wemake_python_styleguide.logic.tree import (
    operators,
)
from wemake_python_styleguide.logic.walk import get_subnodes_by_type
from wemake_python_styleguide.logic.walrus import get_assigned_expr


def get_explicit_as_names(
    node: ast.Match,
) -> Iterable[ast.MatchAs]:
    """
    Returns variable names defined as ``case ... as var_name``.

    Does not return variables defined as ``case var_name``.
    Or in any other forms.
    """
    for match_as in get_subnodes_by_type(node, ast.MatchAs):
        if (
            isinstance(get_parent(match_as), ast.match_case)
            and match_as.pattern
            and match_as.name
        ):
            yield match_as


def is_constant_subject(condition: ast.AST | list[ast.expr]) -> bool:
    """Detect constant subjects for `ast.Match` nodes."""
    if isinstance(condition, list):
        return all(is_constant_subject(node) for node in condition)
    node = operators.unwrap_unary_node(get_assigned_expr(condition))
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, ast.Tuple | ast.List | ast.Set):
        return is_constant_subject(node.elts)
    if isinstance(node, ast.Dict):
        return (
            not any(dict_key is None for dict_key in node.keys)
            and is_constant_subject([
                dict_key for dict_key in node.keys if dict_key is not None
            ])
            and is_constant_subject(node.values)
        )
    return False
