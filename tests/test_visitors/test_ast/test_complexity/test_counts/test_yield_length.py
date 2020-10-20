import pytest

from wemake_python_styleguide.constants import MAX_LEN_YIELD_TUPLE
from wemake_python_styleguide.violations.complexity import (
    TooLongYieldTupleViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    YieldTupleVisitor,
)

generator = """
def function_name():
    i = 0
    while True:
        yield {0}
        i = i + 1
"""

single = 'i + 1'
tuple_empty = '()'
tuple_fixed_long = '(1, 2, 3, 4, 5, 6)'
tuple_fixed_short = '(1, 2, 3)'
tuple_long = 'i, i + 1, i + 2, i + 3, i + 4, i + 5'
tuple_short = 'i, i + 1, i + 2'


@pytest.mark.parametrize('tuple_param', [
    tuple_short,
    single,
    tuple_empty,
    tuple_fixed_short,
])
def test_yield_length_normal(
    assert_errors,
    parse_ast_tree,
    tuple_param,
    mode,
    default_options,
):
    """Testing that classes and functions in a module work well."""
    tree = parse_ast_tree(mode(generator.format(tuple_param)))

    visitor = YieldTupleVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('tuple_param', [
    tuple_long,
    tuple_fixed_long,
])
def test_yield_length_violation(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    tuple_param,
    mode,
    default_options,
):
    """Testing that classes and functions in a module work well."""
    tree = parse_ast_tree(mode(generator.format(tuple_param)))

    visitor = YieldTupleVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooLongYieldTupleViolation])
    assert_error_text(visitor, 6, MAX_LEN_YIELD_TUPLE)
