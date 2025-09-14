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


def is_wildcard_pattern(case: ast.match_case) -> bool:
    """Returns True only for `case _:`."""
    pattern = case.pattern
    return (
        isinstance(pattern, ast.MatchAs)
        and pattern.pattern is None
        and pattern.name is None
    )


def is_simple_pattern(pattern: ast.pattern) -> bool:
    """Returns True if the pattern is simple enough to replace with `==`."""
    return _is_simple_value_or_singleton(pattern) or _is_simple_composite(
        pattern
    )


def _is_simple_composite(pattern: ast.pattern) -> bool:
    """Returns True/False for MatchOr and MatchAs, None otherwise."""
    if isinstance(pattern, ast.MatchOr):
        return all(is_simple_pattern(sub) for sub in pattern.patterns)
    if isinstance(pattern, ast.MatchAs):
        inner = pattern.pattern
        return inner is not None and is_simple_pattern(inner)
    return False


def _is_simple_value_or_singleton(pattern: ast.pattern) -> bool:
    """
    Checks if a pattern is a simple literal or singleton.

    Supports:
    - Single values: ``1``, ``"text"``, ``ns.CONST``.
    - Singleton values: ``True``, ``False``, ``None``.
    """
    if isinstance(pattern, ast.MatchSingleton):
        return True
    if isinstance(pattern, ast.MatchValue):
        return isinstance(
            pattern.value, (ast.Constant, ast.Name, ast.Attribute)
        )
    return False


def is_irrefutable_binding(pattern: ast.pattern) -> bool:
    """
    Returns True for patterns like ``case x:`` or ``case data:``.

    These always match and just bind the subject to a name.
    """
    return (
        isinstance(pattern, ast.MatchAs)
        and pattern.pattern is None
        and pattern.name is not None
    )
