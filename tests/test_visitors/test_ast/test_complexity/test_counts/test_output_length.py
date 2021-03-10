import pytest

from wemake_python_styleguide.constants import MAX_LEN_TUPLE_OUTPUT
from wemake_python_styleguide.violations.complexity import (
    TooLongOutputTupleViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    ReturnLikeStatementTupleVisitor,
)

RETURN_LIKE_STATEMENTS = ('return', 'yield')


generator = """
def function_name():
    i = 0
    while True:
        {0} {1}
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
@pytest.mark.parametrize('return_like', RETURN_LIKE_STATEMENTS)
def test_output_length_normal(
    assert_errors,
    parse_ast_tree,
    tuple_param,
    mode,
    default_options,
    return_like,
):
    """Testing that classes and functions in a module work well."""
    tree = parse_ast_tree(mode(generator.format(return_like, tuple_param)))

    visitor = ReturnLikeStatementTupleVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('tuple_param', [
    tuple_long,
    tuple_fixed_long,
])
@pytest.mark.parametrize('return_like', RETURN_LIKE_STATEMENTS)
def test_output_length_violation(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    tuple_param,
    mode,
    default_options,
    return_like,
):
    """Testing that classes and functions in a module work well."""
    tree = parse_ast_tree(mode(generator.format(return_like, tuple_param)))

    visitor = ReturnLikeStatementTupleVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooLongOutputTupleViolation])
    assert_error_text(visitor, 6, MAX_LEN_TUPLE_OUTPUT)
