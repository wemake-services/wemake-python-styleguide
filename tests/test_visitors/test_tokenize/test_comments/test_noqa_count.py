import pytest

from wemake_python_styleguide.options import defaults
from wemake_python_styleguide.violations.best_practices import (
    OveruseOfNoqaCommentViolation,
)
from wemake_python_styleguide.visitors.tokenize.comments import (
    WrongCommentVisitor,
)


@pytest.mark.parametrize('code', [
    'wallet = 10  # noqa: WPS002,WPS114',
    'wallet = 10  # noqa:WPS002, WPS114',
    'wallet = 10  # noqa: WPS002, WPS114',
    'wallet = 10  # noqa: WPS002',
    'wallet = 1000# noqa: WPS002',
    'wallet = 1000# noqa:  WPS002  ',
])
def test_noqa_overuse(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that `noqa` overuse raises a warning."""
    file_tokens = parse_tokens('{0}\n'.format(code) * (10 + 1))

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [OveruseOfNoqaCommentViolation])


def test_noqa_overuse_is_configurable(
    parse_tokens,
    assert_errors,
    options,
):
    """Ensures that `noqa` overuse can be configured by options."""
    file_tokens = parse_tokens(
        'wallet = 10  # noqa: WPS002, WPS114\n' * defaults.MAX_NOQA_COMMENTS,
    )

    options = options(max_noqa_comments=defaults.MAX_NOQA_COMMENTS - 1)
    visitor = WrongCommentVisitor(options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [OveruseOfNoqaCommentViolation])


def test_noqa_comments_can_be_forbidden(
    parse_tokens,
    assert_errors,
    options,
):
    """Ensures that `noqa` comments can be turned off completely."""
    file_tokens = parse_tokens('wallet = 10  # noqa: WPS002, WPS114')

    options = options(max_noqa_comments=0)
    visitor = WrongCommentVisitor(options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [OveruseOfNoqaCommentViolation])
