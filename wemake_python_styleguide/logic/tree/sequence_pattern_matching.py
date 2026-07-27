import ast
from typing import TypeAlias

_AnySimpleMatchPattern: TypeAlias = (
    ast.MatchValue | ast.MatchSingleton | ast.MatchMapping | ast.MatchSequence
)


def _is_simple_sequence(pattern: ast.MatchSequence) -> bool:
    """Returns True if sequence is simple."""
    for pt in pattern.patterns:
        if not isinstance(pt, _AnySimpleMatchPattern):
            return False
        if (
            isinstance(pt, ast.MatchSequence) and not _is_simple_sequence(pt)
        ) or (isinstance(pt, ast.MatchMapping) and not _is_simple_mapping(pt)):
            return False
    return True


def _is_simple_mapping(pattern: ast.MatchMapping) -> bool:
    """Returns True if all values and keys are simple."""
    if pattern.rest is not None:
        return False
    return _are_keys_simple(pattern) and _are_values_simple(pattern)


def _are_keys_simple(pattern: ast.MatchMapping) -> bool:
    """Returns True if all keys are ``ast.Constant``."""
    return all(isinstance(key, ast.Constant) for key in pattern.keys)


def _are_values_simple(pattern: ast.MatchMapping) -> bool:
    """Returns True if all values are simple."""
    for value_mapping in pattern.patterns:
        if not isinstance(value_mapping, _AnySimpleMatchPattern):
            return False
        if (
            isinstance(value_mapping, ast.MatchMapping)
            and not _is_simple_mapping(value_mapping)
        ) or (
            isinstance(value_mapping, ast.MatchSequence)
            and not _is_simple_sequence(value_mapping)
        ):
            return False
    return True


def is_simple_sequence_or_mapping(pattern: ast.AST) -> bool:
    """Check if pattern is a simple ``ast.Sequence`` or ``ast.Mapping``."""
    if isinstance(pattern, ast.MatchSequence):
        return _is_simple_sequence(pattern)
    if isinstance(pattern, ast.MatchMapping):
        return _is_simple_mapping(pattern)
    return False
