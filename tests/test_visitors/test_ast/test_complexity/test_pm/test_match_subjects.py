import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyMatchSubjectsViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.pm import (
    MatchSubjectsVisitor,
)

match_call_expr = """
match some_call():
    case 1: ...
"""

match_case_long_tuple = """
match some_call['a']:
    case (a, b, c, d, e, f, g, h, i): ...
"""

match_subjects8 = """
match a1, b2, c3, d4, e5, f6, g7, h8:
    case 1: ...
"""

match_subjects7 = """
match a1, b2, c3, d4, e5, f6, g7:
    case 1: ...
"""


def test_match_subjects_wrong_count(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(match_subjects8)

    visitor = MatchSubjectsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyMatchSubjectsViolation])
    assert_error_text(visitor, '8', baseline=default_options.max_match_subjects)


@pytest.mark.parametrize(
    'code',
    [
        match_subjects7,
        match_call_expr,
        match_case_long_tuple,
    ],
)
def test_match_subjects_correct_count(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that default settings do not raise a warning."""
    tree = parse_ast_tree(code)

    visitor = MatchSubjectsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        match_subjects8,
        match_subjects7,
    ],
)
def test_match_subjects_configured_count(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Testing that settings can reflect the change."""
    tree = parse_ast_tree(code)

    option_values = options(max_match_subjects=1)
    visitor = MatchSubjectsVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyMatchSubjectsViolation])
