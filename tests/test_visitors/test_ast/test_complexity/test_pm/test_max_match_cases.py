import pytest

from wemake_python_styleguide.violations.complexity import (
    TooManyMatchCaseViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.pm import (
    MatchCasesVisitor,
)

match_cases1 = """
match x:
    case _: ...
"""

match_cases4 = """
match x:
    case 1: ...
    case 2: ...
    case 3: ...
    case 4: ...
"""

match_cases6 = """
match x:
    case 1: ...
    case 2: ...
    case 3: ...
    case 4: ...
    case 5: ...
    case 6: ...
"""

match_cases7 = """
match x:
    case 1: ...
    case 2: ...
    case 3: ...
    case 4: ...
    case 5: ...
    case 6: ...
    case 7: ...
"""


@pytest.mark.parametrize(
    'code',
    [
        match_cases7,
    ],
)
def test_match_cases_wrong_count(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that default settings raise a warning."""
    tree = parse_ast_tree(code)

    visitor = MatchCasesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyMatchCaseViolation])
    assert_error_text(visitor, '7', baseline=default_options.max_match_cases)


@pytest.mark.parametrize(
    'code',
    [
        match_cases1,
        match_cases6,
    ],
)
def test_match_cases_correct_count(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that default settings do not raise a warning."""
    tree = parse_ast_tree(code)

    visitor = MatchCasesVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        match_cases4,
        match_cases6,
        match_cases7,
    ],
)
def test_match_cases_configured_count(
    assert_errors,
    parse_ast_tree,
    code,
    options,
):
    """Testing that settings can reflect the change."""
    tree = parse_ast_tree(code)

    option_values = options(max_match_cases=2)
    visitor = MatchCasesVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooManyMatchCaseViolation])
