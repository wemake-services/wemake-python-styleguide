import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongMagicCommentViolation,
)
from wemake_python_styleguide.visitors.tokenize.comments import NoqaVisitor


@pytest.mark.parametrize('code', [
    'x = 10_00  # noqa: WPS002,Z114',
    'x = 10_00  # noqa:A002, U114',
    'x = 10_00  # noqa: J002, WPS114',
    'wallet = 10_00  # noqa: CPP002',
    'x = 1000  # noqa: DJ002',
    'x = 1000  # noqa:  WPS002  ',
    'print(12 + 3)  # regular comment',
    'print(12 + 3)  #',
    'print(12 + 3)',
    '',
])
def test_correct_comments(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct comments do not raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = NoqaVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    'x = 10_00 # noqa WPS002',
    'x = 10_00  # noqa',
    'x = 10_00  #   noqa   ',
    'x = 10_00 #noqa',
    'x = 10_00#noqa',
    'wallet = 10_00  # noqa: some comments',
    'x = 1000  # noqa:',
    'x = 10_00 # noqa: -',
    'x = 10_00 # noqa: *',
    '# noqa',
])
def test_incorrect_noqa_comment(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that incorrect `noqa` comments raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = NoqaVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [WrongMagicCommentViolation])
