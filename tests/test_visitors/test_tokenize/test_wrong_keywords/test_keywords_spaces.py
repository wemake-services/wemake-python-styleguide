# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    MissingSpaceBetweenKeywordAndParenViolation,
)
from wemake_python_styleguide.visitors.tokenize.keywords import (
    WrongKeywordTokenVisitor,
)


@pytest.mark.parametrize('code', [
    'del(a)',
    'for(a, b) in [(1, 2)]:',
    'for (a, b) in((1, 2)):',
    'if a in(1, 2, 3):',
    'assert(\n'
    '    1, 2, 3,\n'
    ') in b',
    'def foo():\n'
    '    yield(1, 2, 3)',
])
def test_missing_space(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that paren right after keyword raises a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongKeywordTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [MissingSpaceBetweenKeywordAndParenViolation])


@pytest.mark.parametrize('code', [
    'del (a, b)',
    'for (a, b) in (1, 2, 3)',
    'def foo():\n'
    '    yield (1, 2, 3)',
])
def test_fine_when_space_in_between_keyword_and_paren(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that there's no violation if space in between."""
    file_tokens = parse_tokens(code)

    visitor = WrongKeywordTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
