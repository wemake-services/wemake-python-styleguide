# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.errors.best_practices import (
    WrongMagicCommentViolation,
)
from wemake_python_styleguide.visitors.tokenize.wrong_comments import (
    WrongCommentVisitor,
)


@pytest.mark.parametrize('code', [
    '1 + "12"  # type: ignore',
    '1 + "12"  # type:ignore',
    'total = 1000  # type is not clear',
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
    'total = 1000  # type: int',
    'total = 1000  # type:int',
    'total = 1000 # type: int  ',
    'total = 1000#type:int',
    'numbs = [1, 2, 3]  # type: missing',
    'numbs = [1, 2, 3]  # type: List[int]',
    'numbs = [1, 2, 3]  # type: List["int"]',
    "numbs = [1, 2, 3]  # type: List['int']",
    'field = SomeField()  # type: drf.Field',
    '# type: fixme',
])
def test_incorrect_type_comment(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that incorrect `type` comments raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [WrongMagicCommentViolation])
