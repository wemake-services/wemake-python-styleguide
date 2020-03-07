import pytest

from wemake_python_styleguide.violations.refactoring import (
    ImplicitInConditionViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    ImplicitBoolPatternsVisitor,
)

# Correct:

eq_and = '{0} == some1 and {1} == some2'
noteq_or = '{0} != some1 or {1} != some2'

# Wrong:

eq_or = '{0} == some1 or {1} == some2'
noteq_and = '{0} != some1 and {1} != some2'


@pytest.mark.parametrize('code', [
    eq_and,
    noteq_or,
    eq_or,
    noteq_and,
])
@pytest.mark.parametrize(('first', 'second'), [
    ('first', 'second'),
    ('one.attr', 'one'),
    ('first', 'first()'),
    ('value.method()', 'value.method'),
    ('value.method(1)', 'value.method(2)'),
])
def test_different_in_values(
    code,
    first,
    second,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing regular conditions."""
    tree = parse_ast_tree(code.format(first, second))

    visitor = ImplicitBoolPatternsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    eq_and,
    noteq_or,
])
@pytest.mark.parametrize(('first', 'second'), [
    ('first', 'first'),
    ('one.attr', 'one.attr'),
    ('first()', 'first()'),
    ('value.method(1)', 'value.method(2)'),
])
def test_safe_patterns_in_values(
    code,
    first,
    second,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing safe in patterns."""
    tree = parse_ast_tree(code.format(first, second))

    visitor = ImplicitBoolPatternsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    eq_or,
    noteq_and,
])
@pytest.mark.parametrize(('first', 'second'), [
    ('first', 'first'),
    ('one.attr', 'one.attr'),
    ('first()', 'first()'),
    ('value.method(1)', 'value.method(1)'),
])
def test_wrong_patterns_in_values(
    code,
    first,
    second,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing safe in patterns."""
    tree = parse_ast_tree(code.format(first, second))

    visitor = ImplicitBoolPatternsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ImplicitInConditionViolation])
