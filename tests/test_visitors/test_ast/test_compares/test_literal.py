import pytest

from wemake_python_styleguide.violations.consistency import (
    ConstantCompareViolation,
    ReversedComplexCompareViolation,
)
from wemake_python_styleguide.visitors.ast.compares import CompareSanityVisitor

chained_compares1 = '0 < {0} < {1}'
chained_compares2 = '{0} > {1} > 0'
chained_compares3 = '-1 > {0} > {1} > 0'

walrus_compares1 = '(x := {0}) > {1} > 1'
walrus_compares2 = '{0} > (x := {1}) > 1'


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
    chained_compares1,
    chained_compares3,
])
@pytest.mark.parametrize('comparators', [
    (1, 'first_name'),
    (1, 1),
])
def test_literal_special1(
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
    chained_compares2,
    chained_compares3,
    walrus_compares1,
    walrus_compares2,
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
        ignored_types=ReversedComplexCompareViolation,
    )


@pytest.mark.parametrize('code', [
    chained_compares1,
    chained_compares2,
    chained_compares3,
    walrus_compares1,
    walrus_compares2,
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

    assert_errors(
        visitor,
        [],
        ignored_types=ReversedComplexCompareViolation,
    )
