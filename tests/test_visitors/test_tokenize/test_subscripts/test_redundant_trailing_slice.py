import pytest

from wemake_python_styleguide.violations.consistency import (
    RedundantTrailingSliceViolation,
)
from wemake_python_styleguide.visitors.tokenize.subscripts import (
    RedundantTrailingSliceVisitor,
)

# Wrong:
trailing_colon_cases = [
    'a[1:4:]',
    'a[1::]',
    'a[:4:]',
    'a[None::]',
    'a[1:None:]',
    'a[1 + 2::]',
]

# Correct:
correct_cases = [
    'a[1:4]',
    'a[1:]',
    'a[:4]',
    'a[::]',           # caught by NonStrictSliceOperationsViolation
    'a[1:4:5]',
    'a[1:4:None]',
    'a[1]',
    'a[1:4:1]',        # caught by RedundantSubscriptViolation, not ours
    'a[b[1:4:5]]',     # nested valid slice
    'a[b[1:4:]]',      # nested invalid — should flag inner
    'a[{1: 2}]',       # dict literal inside subscript
    'a[(1, 2)]',       # tuple inside subscript
    'a[lambda x: x]',  # lambda inside subscript
]


@pytest.mark.parametrize('code', trailing_colon_cases)
def test_redundant_trailing_colon(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensure trailing colon in slice is forbidden."""
    file_tokens = parse_tokens(code)
    visitor = RedundantTrailingSliceVisitor(
        default_options,
        file_tokens=file_tokens,
    )
    visitor.run()
    assert_errors(visitor, [RedundantTrailingSliceViolation])


@pytest.mark.parametrize('code', correct_cases)
def test_correct_slice_not_flagged(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensure valid slices do not raise violation."""
    file_tokens = parse_tokens(code)
    visitor = RedundantTrailingSliceVisitor(
        default_options,
        file_tokens=file_tokens,
    )
    visitor.run()
    assert_errors(visitor, [])
