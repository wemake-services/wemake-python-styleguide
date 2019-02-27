# -*- coding: utf-8 -*-

import pytest

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
    default_options,
    code,
):
    """Ensures that `no cover` overuse raises a warning."""
    file_tokens = parse_tokens((code + '\n') * (5 + 1))

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [OveruseOfNoCoverCommentViolation])
