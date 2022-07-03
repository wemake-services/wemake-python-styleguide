import pytest

from wemake_python_styleguide.violations.complexity import (
    TooLongTupleUnpackViolation,
)
from wemake_python_styleguide.visitors.ast.complexity.counts import (
    TupleUnpackVisitor,
)

short_unpack = 'a, b = (1, 2)'
short_starred_unpack = 'a, b, *rest = (1, 2, 3, 4, 5)'
single_unpack = 'result = (1, 2, 3, 4, 5)'
function_unpack = 'result = some()'
class_attr_unpack = """
class foo(object):
    result = (1, 2, 3, 4, 5)
"""

long_unpack = 'a, b, c, d, e = (1, 2, 3, 4, 5)'
long_starred_unpack = 'a, b, c, d, *rest = (1, 2, 3, 4, 5, 6)'
long_function_unpack = 'a, b, c, d, e = some()'
long_class_attr_unpack = """
class foo(object):
    a, b, c, d, e = (1, 2, 3, 4, 5)
"""


@pytest.mark.parametrize('unpack_expression', [
    short_unpack,
    short_starred_unpack,
    single_unpack,
    function_unpack,
    class_attr_unpack,
])
def test_unpack_length_normal(
    assert_errors,
    parse_ast_tree,
    unpack_expression,
    options,
):
    """Test that correct usage of unpack expression don't raise exceptions."""
    tree = parse_ast_tree(unpack_expression)

    option_values = options(max_tuple_unpack_length=4)
    visitor = TupleUnpackVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('unpack_expression', [
    long_unpack,
    long_starred_unpack,
    long_function_unpack,
    long_class_attr_unpack,
])
def test_unpack_length_violation(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    unpack_expression,
    options,
):
    """Test that violations raise proper exceptions."""
    tree = parse_ast_tree(unpack_expression)

    option_values = options(max_tuple_unpack_length=4)
    visitor = TupleUnpackVisitor(option_values, tree=tree)
    visitor.run()

    assert_errors(visitor, [TooLongTupleUnpackViolation])
    assert_error_text(visitor, 5, option_values.max_tuple_unpack_length)
