import pytest

from wemake_python_styleguide.constants import MAX_NO_COVER_COMMENTS
from wemake_python_styleguide.violations.best_practices import (
    OveruseOfNoCoverCommentViolation,
)
from wemake_python_styleguide.visitors.tokenize.comments import (
    WrongCommentVisitor,
)


@pytest.mark.parametrize('code', [
    'wallet = 10  # pragma: no cover',
    'wallet = 10  # pragma: no  cover',
    'wallet = 10  # pragma:  no  cover',
    'wallet = 10  # pragma:  no cover',
])
def test_no_cover_overuse(
    parse_tokens,
    assert_errors,
    assert_error_text,
    default_options,
    code,
):
    """Ensures that `no cover` overuse raises a warning."""
    file_tokens = parse_tokens('{0}\n'.format(code) * (5 + 1))

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [OveruseOfNoCoverCommentViolation])
    assert_error_text(visitor, '6', MAX_NO_COVER_COMMENTS)
