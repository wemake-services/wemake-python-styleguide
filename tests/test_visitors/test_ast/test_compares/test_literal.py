import pytest

from wemake_python_styleguide.violations.consistency import (
    ConstantCompareViolation,
    ReversedComplexCompareViolation,
)
from wemake_python_styleguide.visitors.ast.compares import CompareSanityVisitor

if_with_chained_compares1 = 'if 0 < {0} < {1}: ...'
if_with_chained_compares2 = 'if {0} > {1} > 0: ...'
if_with_chained_compares3 = 'if -1 > {0} > {1} > 0: ...'


@pytest.mark.filterwarnings('ignore::SyntaxWarning')
@pytest.mark.parametrize('comparators', [
    ('first_name', 'second_name'),
    ('first_name', 1),
    (1, 'first_name'),
])
def test_non_literal(
    assert_errors,
    parse_ast_tree,
    simple_conditions,
    comparators,
    default_options,
):
    """Testing that compares work well."""
    tree = parse_ast_tree(simple_conditions.format(*comparators))

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.filterwarnings('ignore::SyntaxWarning')
@pytest.mark.parametrize('comparators', [
    (1, 2),
    ('"string1"', '"string2"'),
    ('[1, 2, 3]', '(1, 2, 3)'),
    ('{"key": 1}', '{"a", "b"}'),
])
def test_literal(
    assert_errors,
    parse_ast_tree,
    simple_conditions,
    comparators,
    default_options,
):
    """Testing that violations are when using literal compares."""
    tree = parse_ast_tree(simple_conditions.format(*comparators))

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConstantCompareViolation])


@pytest.mark.parametrize('code', [
    if_with_chained_compares1,
    if_with_chained_compares3,
])
@pytest.mark.parametrize('comparators', [
    (1, 'first_name'),
    (1, 1),
])
def test_literal_special(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Testing that special cases do work and raise warnings."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ConstantCompareViolation])


@pytest.mark.parametrize('code', [
    if_with_chained_compares2,
    if_with_chained_compares3,
])
@pytest.mark.parametrize('comparators', [
    ('first_name', 1),
    (1, 1),
])
def test_literal_special2(
    assert_errors,
    parse_ast_tree,
    code,
    comparators,
    default_options,
):
    """Testing that special cases do work and raise warnings."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [ConstantCompareViolation],
        ReversedComplexCompareViolation,
    )


@pytest.mark.parametrize('code', [
    if_with_chained_compares1,
    if_with_chained_compares2,
    if_with_chained_compares3,
])
def test_literal_special_without_errors(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that special cases do work and do not raise warnings."""
    tree = parse_ast_tree(code.format('first_name', 'second_name'))

    visitor = CompareSanityVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [], ReversedComplexCompareViolation)
