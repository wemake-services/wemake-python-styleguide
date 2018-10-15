# -*- coding: utf-8 -*-

import sys

import pytest

from wemake_python_styleguide.violations.consistency import (
    MissingSpaceBetweenKeywordAndParenViolation,
)
from wemake_python_styleguide.visitors.tokenize.keywords import (
    WrongKeywordTokenVisitor,
)

_multiline_error_function = """
def foo():
    yield(1, 2, 3)
"""
_multiline_error_statement = """
assert(
    1, 2, 3,
) in b,
"""


@pytest.mark.parametrize('code', [
    'del(a)',
    'for(a, b) in [(1, 2)]:',
    'for (a, b) in((1, 2)):',
    'if a in(1, 2, 3):',
    'return(a)',
    pytest.param(
        'await(a)',
        marks=pytest.mark.skipif(
            sys.version_info < (3, 7),
            reason='await is a keyword only since py3.7',
        ),
    ),
    'with(lambda x: x)() as (a, b)',
    'with (lambda x: x)() as(a, b)',
    '(a, b) is(a, b)',
    'from foo import(bar, baz, spam)',
    'except(ValueError, KeyError)',
    'elif(bar, baz)',
    'else(bar, baz)',
    _multiline_error_function,
    _multiline_error_statement,
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


_multiline_correct_function = """
def foo():
    yield (1, 2, 3)
"""
_multiline_correct_statement = """
assert (
    1, 2, 3,
) in b,
"""


@pytest.mark.parametrize('code', [
    'del (a, b)',
    'for (a, b) in (1, 2, 3)',
    'return (a)',
    pytest.param(
        'await (a)',
        marks=pytest.mark.skipif(
            sys.version_info < (3, 7),
            reason='await is a keyword only since py3.7',
        ),
    ),
    'with do_things() as (a, b)',
    '(a, b) is (a, b)',
    'from foo import (bar, baz, spam)',
    'except (ValueError, KeyError)',
    'elif (bar, baz)',
    'else (bar, baz)',
    _multiline_correct_function,
    _multiline_correct_statement,
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
