import ast


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
    Check that all elements in sequence/mapping are simple.

    Simple is (literals, constants, names).
    """
    if isinstance(pattern, ast.MatchSequence):
        return all(is_simple_pattern(pattern) for pattern in pattern.patterns)
    if isinstance(pattern, ast.MatchMapping):
        return all(is_simple_pattern(pattern) for pattern in pattern.patterns)
    return False
