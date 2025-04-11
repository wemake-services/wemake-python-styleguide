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
        'items[None::-1]',
        'items[:None:-1]',
        'items[None:None:-1]',
        'items[-1::-1]',
        'items[-1:None:-1]',
        # copy
        'items[:]',
        'items[None:]',
        'items[:None]',
        'items[None:None]',
        'items[::]',
        'items[None::]',
        'items[:None:]',
        'items[::None]',
        'items[None:None:]',
        'items[None::None]',
        'items[:None:None]',
        'items[None:None:None]',
        'items[::1]',
        'items[None::1]',
        'items[:None:1]',
        'items[None:None:1]',
        'items[0:]',
        'items[0:None]',
        'items[0::]',
        'items[0:None:]',
        'items[0::None]',
        'items[0:None:None]',
        'items[0:None:1]',
        # pop
        'items[:-1]',
        'items[None:-1]',
        'items[None:-1:None]',
        'items[0:-1]',
        'items[0:-1:None]',
        'items[:-1:]',
        'items[None:-1:]',
        'items[:-1:None]',
        'items[0:-1:1]',
        'items[None:-1:1]',
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
        # pop
        'other = items[:-1]',
        # other
        'items[0]',
        'items[:2]',
        'items[0:]',
        'items[1::-1]',
        'items[1:4:-1]',
        'items[:x]',
        'items[:-x]',
        'items[::-x]',
        'items[::x]',
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
