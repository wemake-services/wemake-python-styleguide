# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    WrongUnicodeEscapeViolation,
)
from wemake_python_styleguide.violations.consistency import (
    UnicodeStringViolation,
    UppercaseStringModifierViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongStringTokenVisitor,
)


@pytest.mark.parametrize('code', [
    r"b'\ua'",
    r"b'\u1'",
    r"b'\Ua'",
    r"b'\N{GREEK SMALL LETTER ALPHA}'",
])
def test_wrong_unicode_escape(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that wrong unicode escape raises a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [WrongUnicodeEscapeViolation])


@pytest.mark.parametrize('code', [
    r"'\ua'",
    r"'\u1'",
    r"'\Ua'",
    r"'\N{GREEK SMALL LETTER ALPHA}'",
])
def test_correct_unicode_escape(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct unicode escape does not raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    r"u'\ua'",
    r"u'\u1'",
    r"u'\Ua'",
    r"u'\N{GREEK SMALL LETTER ALPHA}'",
])
def test_correct_unicode_string_escape(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct unicode escape does not raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [UnicodeStringViolation])


@pytest.mark.parametrize('code', [
    r"U'\ua'",
    r"U'\u1'",
    r"U'\Ua'",
    r"U'\N{GREEK SMALL LETTER ALPHA}'",
])
def test_correct_unicode_upper_string_escape(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct unicode escape does not raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [
        UnicodeStringViolation,
        UppercaseStringModifierViolation,
    ])
