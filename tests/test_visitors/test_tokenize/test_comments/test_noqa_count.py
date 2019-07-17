# -*- coding: utf-8 -*-

import pytest

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
    file_tokens = parse_tokens((code + '\n') * (10 + 1))

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [OveruseOfNoqaCommentViolation])
