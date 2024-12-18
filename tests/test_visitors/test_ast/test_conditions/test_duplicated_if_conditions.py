import pytest

from wemake_python_styleguide.violations.refactoring import (
    DuplicateIfConditionViolation,
    NegatedConditionsViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import IfStatementVisitor

# Always correct:

if_simple = """
if {0}:
    ...
"""

if_and_else = """
if {0}:
    ...
else:
    ...
"""

if_after_if = """
if {0}:
    ...
if {0}:
    ...
"""

# Can be duplicated:

if_and_elif1 = """
if {0}:
    ...
elif {1}:
    ...
"""

if_and_elif2 = """
if {0}:
    ...
elif will_be_hard_to_match.custom():
    ...
elif {1}:
    ...
"""

if_and_elif3 = """
if {0}:
    ...
elif {1}:
    ...
else:
    ...
"""

# Duplicating twice should raise twice:
if_two_dups = """
if noqa_wps533:
    my_print('1')
elif noqa_wps533:
    my_print('2')
elif noqa_wps533:
    my_print('3')
"""

# List of conditions to test:
conditions = [
    'not some',
    '-some',
    'some != 1',
    'some',
    'some.method()',
    'some.attr',
    'some[index]',
    'some == 0',
    'some != other',
    'some > 1',
    '(func := method()) and func > 0',
]


@pytest.mark.parametrize(
    'template',
    [
        if_simple,
        if_and_else,
        if_after_if,
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

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [], ignored_types=NegatedConditionsViolation)


@pytest.mark.parametrize(
    'template',
    [
        if_and_elif1,
        if_and_elif2,
        if_and_elif3,
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
    tree = parse_ast_tree(template.format(code, 'some.method(different_arg)'))

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [], ignored_types=NegatedConditionsViolation)


@pytest.mark.parametrize(
    'template',
    [
        if_and_elif1,
        if_and_elif2,
        if_and_elif3,
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

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [DuplicateIfConditionViolation],
        ignored_types=NegatedConditionsViolation,
    )
    assert_error_text(visitor, code, ignored_types=NegatedConditionsViolation)


@pytest.mark.parametrize(
    'code',
    [
        if_two_dups,
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

    visitor = IfStatementVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [DuplicateIfConditionViolation, DuplicateIfConditionViolation],
    )
