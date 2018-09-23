# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.tokenize.wrong_primitives import (
    UnicodeStringViolation,
    WrongPrimitivesVisitor,
)


@pytest.mark.parametrize('code', [
    'x = u"text"',
    "print(u'unicode')",
    '"3_3" + u"5_5"',
])
def test_unicode_prefix(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that unicode prefixes raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [UnicodeStringViolation])


@pytest.mark.parametrize('code', [
    'x = "name"',
    'x = r"text"',
    "print(b'unicode')",
    '"u" + "12"',
])
def test_correct_strings(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct strings are fine."""
    file_tokens = parse_tokens(code)

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
