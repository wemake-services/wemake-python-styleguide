import pytest

from wemake_python_styleguide.violations.refactoring import (
    DuplicateCasePatternViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import MatchVisitor

# Always correct:

match_single = """
match some_value:
    case {0}:
        ...
"""

match_after_match = """
match some_value:
    case {0}:
        ...
match some_value:
    case {0}:
        ...
"""

# Can be duplicated:

match_with_two_cases1 = """
match some_value:
    case {0}:
        ...
    case {1}:
        ...
"""

match_with_two_cases2 = """
match some_value:
    case {0}:
        ...
    case will_be_hard_to_match():
        ...
    case {1}:
        ...
"""

# Duplicating twice should raise twice:
match_two_dups = """
match some_value:
    case SomeClass(field) if field > 0: ...
    case SomeClass(field) if field > 0: ...
    case OtherClass(): ...
    case OtherClass(): ...
"""

# List of conditions to test:
conditions = [
    'SomeClass(field)',
    'SomeClass(field) if field > 0',
    'SomeClass(field) as named if field > 0',
    '[some]',
    '{}',
    "{'key': some} if check(some)",
    'FirstClass(x) | [x]',
    "['first', [x] as lst]",
]


@pytest.mark.parametrize(
    'template',
    [
        match_single,
        match_after_match,
    ],
)
@pytest.mark.parametrize(
    'code',
    conditions,
)
def test_always_correct_conditions(
    template,
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing simple conditions."""
    tree = parse_ast_tree(template.format(code))

    visitor = MatchVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'template',
    [
        match_with_two_cases1,
        match_with_two_cases2,
    ],
)
@pytest.mark.parametrize(
    'code',
    conditions,
)
def test_different_conditions(
    template,
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that different conditions produce no errors."""
    tree = parse_ast_tree(template.format(code, 'some_test_other_value'))

    visitor = MatchVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'template',
    [
        match_with_two_cases1,
        match_with_two_cases2,
    ],
)
@pytest.mark.parametrize(
    'code',
    conditions,
)
def test_same_conditions(
    template,
    code,
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
):
    """Testing that same conditions trigger a violation."""
    tree = parse_ast_tree(template.format(code, code))

    visitor = MatchVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [DuplicateCasePatternViolation],
    )
    assert_error_text(visitor, code)


@pytest.mark.parametrize(
    'code',
    [
        match_two_dups,
    ],
)
def test_two_duplicate_conditions(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that same conditions trigger a violation."""
    tree = parse_ast_tree(code)

    visitor = MatchVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [DuplicateCasePatternViolation, DuplicateCasePatternViolation],
    )
