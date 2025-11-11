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


def is_simple_sequence_or_mapping_pattern(pattern: ast.pattern) -> bool:
    """
    Checks if a pattern is a simple sequence or mapping without
    variable bindings.

    Supports:
    - Simple lists: ``[1, 2]``, ``["a", "b"]``, ``[const.A, const.B]``
    - Simple tuples: ``(1, 2)``, ``("a", "b")``
    - Simple dicts: ``{"key": "value"}``, ``{1: 2}``
    - No variable bindings (like ``[x, y]``) or starred patterns
      (like ``[first, *rest]``)
    - No guards allowed
    """
    # Check for simple list or tuple patterns
    if isinstance(pattern, ast.MatchSequence):
        # Check that there are no starred patterns (*rest)
        if not _has_star_pattern(pattern):
            # Check that all elements are simple patterns (not binding vars)
            return all(
                _is_simple_pattern_element(element)
                for element in pattern.patterns
            )

    # Check for simple dict patterns
    elif isinstance(pattern, ast.MatchMapping):
        # Check that all keys are simple (not variables) and all
        # values are simple patterns
        if any(
            key is None or not _is_simple_key_pattern(key)
            for key in pattern.keys
        ):
            return False
        if pattern.patterns and any(
            not _is_simple_pattern_element(value) for value in pattern.patterns
        ):
            return False
        # If rest name is present (has variable binding), it's not simple
        return pattern.rest is None

    return False


def _has_star_pattern(pattern: ast.MatchSequence) -> bool:
    """Check if the sequence pattern contains starred patterns."""
    # ast.MatchStar has been added in Python 3.10 for starred patterns
    for sub_pattern in pattern.patterns:
        if isinstance(sub_pattern, ast.MatchStar):
            return True
    return False


def _is_simple_pattern_element(pattern: ast.pattern) -> bool:
    """Check if a pattern element is simple (not binding variables)."""
    # Handle simple value patterns (literals, constants, attributes)
    if isinstance(pattern, ast.MatchValue):
        return isinstance(
            pattern.value, (ast.Constant, ast.Name, ast.Attribute)
        )

    # Handle simple singleton patterns (True, False, None)
    if isinstance(pattern, ast.MatchSingleton):
        return True

    # Handle simple nested patterns
    if isinstance(pattern, (ast.MatchSequence, ast.MatchMapping)):
        return is_simple_sequence_or_mapping_pattern(pattern)

    # Handle Union patterns (| operator)
    if isinstance(pattern, ast.MatchOr):
        return all(_is_simple_pattern_element(sub) for sub in pattern.patterns)

    # Handle MatchAs patterns - not simple if it's binding a variable
    if isinstance(pattern, ast.MatchAs):
        # If pattern.name is not None, it's a binding (not simple)
        if pattern.name is not None:
            return False
        # If pattern.name is None but pattern.pattern is not None,
        # check if the inner pattern is simple
        if pattern.pattern is not None:
            return _is_simple_pattern_element(pattern.pattern)
        # This case should not happen in valid Python ASTs
        return False

    # Other pattern types are not simple (like MatchClass with constructors)
    return False


def _is_simple_key_pattern(key: ast.expr) -> bool:
    """Check if a mapping key is simple (not a variable)."""
    # Keys should be constants or attributes, not variable names
    return isinstance(key, (ast.Constant, ast.Name, ast.Attribute))
