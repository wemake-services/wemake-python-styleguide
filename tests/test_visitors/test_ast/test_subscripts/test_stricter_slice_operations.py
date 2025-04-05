import pytest

from wemake_python_styleguide.violations.best_practices import (
    NonStrictSliceOperationsViolation,
)
from wemake_python_styleguide.visitors.ast.subscripts import (
    StricterSliceOperations,
)


@pytest.mark.parametrize(
    'expression',
    [
        # reverse
        'items[::-1]',
        # copy
        'other = items[:]',
        'other = items[::]',
        # pop
        'items = items[:-1]',
        'some, items = "some", items[:-1]',
    ],
)
def test_non_strict_slice_operation_bad(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing for using non strict slice operations."""
    tree = parse_ast_tree(expression)

    visitor = StricterSliceOperations(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [NonStrictSliceOperationsViolation])


@pytest.mark.parametrize(
    'expression',
    [
        # copy
        'items[::]',
        'items[:]',
        # pop
        'other = items[:-1]',
        # other
        'items[0]',
        'items[:2]',
        'a = items[1::-1]',
        'a = items[0]',
    ],
)
def test_non_strict_slice_operation_good(
    assert_errors,
    parse_ast_tree,
    expression,
    default_options,
):
    """Testing for using non strict slice operations."""
    tree = parse_ast_tree(expression)

    visitor = StricterSliceOperations(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
