import pytest

from wemake_python_styleguide.violations.consistency import (
    ImplicitComplexCompareViolation,
)
from wemake_python_styleguide.visitors.ast.conditions import (
    ImplicitBoolPatternsVisitor,
)

# Won't match our rule with any values:

less_or_less = '{0} < {1} or {2} < {3}'
less_or_more = '{0} < {1} or {2} > {3}'
more_or_more = '{0} > {1} or {2} > {3}'

lesseq_or_less = '{0} <= {1} or {2} < {3}'
less_or_lesseq = '{0} < {1} or {2} <= {3}'
lesseq_or_lesseq = '{0} <= {1} or {2} <= {3}'

lesseq_or_more = '{0} <= {1} or {2} > {3}'
less_or_moreeq = '{0} < {1} or {2} >= {3}'
lesseq_or_moreeq = '{0} <= {1} or {2} >= {3}'

moreeq_or_more = '{0} >= {1} or {2} > {3}'
more_or_moreeq = '{0} > {1} or {2} >= {3}'
moreeq_or_moreeq = '{0} >= {1} or {2} >= {3}'

# Will match our rule with some values:

more_and_more = '{0} > {1} and {2} > {3}'  # a > b > c
less_and_less = '{0} < {1} and {2} < {3}'  # a < b < c
less_and_more = '{0} < {1} and {2} > {3}'  # a < b < c
more_and_less = '{0} > {1} and {2} < {3}'  # a > b > c

moreeq_and_more = '{0} >= {1} and {2} > {3}'
more_and_moreeq = '{0} > {1} and {2} >= {3}'
moreeq_and_moreeq = '{0} >= {1} and {2} >= {3}'

lesseq_and_less = '{0} <= {1} and {2} < {3}'
less_and_lesseq = '{0} < {1} and {2} <= {3}'
lesseq_and_lesseq = '{0} <= {1} and {2} <= {3}'

lesseq_and_more = '{0} <= {1} and {2} > {3}'
less_and_moreeq = '{0} < {1} and {2} >= {3}'
lesseq_and_moreeq = '{0} <= {1} and {2} >= {3}'

moreeq_and_less = '{0} >= {1} and {2} < {3}'
more_and_lesseq = '{0} > {1} and {2} <= {3}'
moreq_and_lesseq = '{0} >= {1} and {2} <= {3}'


@pytest.mark.parametrize('code', [
    more_and_more,
    less_and_less,

    moreeq_and_more,
    more_and_moreeq,
    moreeq_and_moreeq,

    lesseq_and_less,
    less_and_lesseq,
    lesseq_and_lesseq,
])
@pytest.mark.parametrize('comparators', [
    ('a', 'b', 'b', 'c'),
    ('a', 'b', 'b', '10'),
    ('a()', 'b', 'b', 'c'),
    ('a', 'b', 'b', 'c(1, 2, 3)'),
    ('a(None)', 'b', 'b', 'c()'),
    ('a.prop', 'b', 'b', 'c.method()'),
    ('a("string")', 'b', 'b', '2'),
    ('a', 'b', 'b', 'c and other == 1'),
    ('a', 'b and other == 1', 'b', 'c'),
    ('1', 'a', 'a', '10'),
    ('1', 'a', 'a', 'b'),
    ('1', 'a', 'a', '10 and call()'),
])
def test_implicit_complex_compare(
    code,
    comparators,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing implicit complex compare."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = ImplicitBoolPatternsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ImplicitComplexCompareViolation])


@pytest.mark.parametrize('code', [
    less_and_more,
    lesseq_and_more,
    less_and_moreeq,
    lesseq_and_moreeq,

    more_and_less,
    moreeq_and_less,
    more_and_lesseq,
    moreq_and_lesseq,
])
@pytest.mark.parametrize('comparators', [
    ('a', 'b', 'c', 'b'),
    ('a', 'b', 'c(k, v)', 'b'),
    ('a(1)', 'b', 'c', 'b'),
    ('a', 'b', 'c.attr', 'b'),
    ('a.method()', 'b', 'c', 'b'),
    ('a.method(value)', 'b', '1', 'b'),
    ('a', 'b', '10', 'b'),
    ('1', 'b', 'c', 'b'),
    ('1', 'b', '10', 'b'),
    ('a', 'b', 'c', 'b and other == 1'),
])
def test_implicit_complex_compare_reversed(
    code,
    comparators,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing implicit complex compare."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = ImplicitBoolPatternsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [ImplicitComplexCompareViolation])


@pytest.mark.parametrize('code', [
    more_and_more,
    moreeq_and_more,
    more_and_moreeq,
    moreeq_and_moreeq,

    less_and_less,
    lesseq_and_less,
    less_and_lesseq,
    lesseq_and_lesseq,

    less_and_more,
    lesseq_and_more,
    less_and_moreeq,
    lesseq_and_moreeq,

    more_and_less,
    moreeq_and_less,
    more_and_lesseq,
    moreq_and_lesseq,
])
@pytest.mark.parametrize('comparators', [
    ('a', 'None', 'b', 'c'),
])
def test_compare_wrong_values(
    code,
    comparators,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing implicit complex compare."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = ImplicitBoolPatternsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    less_or_less,
    less_or_more,
    more_or_more,

    lesseq_or_less,
    less_or_lesseq,
    lesseq_or_lesseq,

    lesseq_or_more,
    less_or_moreeq,
    lesseq_or_moreeq,

    moreeq_or_more,
    more_or_moreeq,
    moreeq_or_moreeq,
])
@pytest.mark.parametrize('comparators', [
    ('a', 'b', 'b', 'c'),
    ('a', 'b', 'a', 'c'),
    ('a', 'c', 'b', 'c'),
    ('a', '1', 'a', '2'),
    ('a', 'b', 'b', 'c and other == 1'),
])
def test_regular_compare(
    code,
    comparators,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing implicit complex compare."""
    tree = parse_ast_tree(code.format(*comparators))

    visitor = ImplicitBoolPatternsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    'a < b',
    'a > c',
    'a and b',
    'a or c',
    'not a',
])
def test_regular_short_compare(
    code,
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing implicit complex compare."""
    tree = parse_ast_tree(code)

    visitor = ImplicitBoolPatternsVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
