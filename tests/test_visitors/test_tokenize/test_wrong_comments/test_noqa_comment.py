# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongMagicCommentViolation,
)
from wemake_python_styleguide.visitors.tokenize.comments import (
    WrongCommentVisitor,
)


@pytest.mark.parametrize('code', [
    'x = 10_00  # noqa: Z002,Z114',
    'x = 10_00  # noqa:Z002, Z114',
    'x = 10_00  # noqa: Z002, Z114',
    'wallet = 10_00  # noqa: Z002',
    'x = 1000  # noqa: Z002',
    'x = 1000  # noqa:  Z002  ',
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

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
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

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [WrongMagicCommentViolation])
