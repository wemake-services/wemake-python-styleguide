# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    UnicodeStringViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongPrimitivesVisitor,
)


@pytest.mark.parametrize('primitive', [
    'u"text"',
    "u'unicode'",
    'u"5_5"',
    'u""',
])
def test_unicode_prefix(
    parse_tokens,
    assert_errors,
    assert_error_text,
    default_options,
    primitives_usages,
    primitive,
    mode,
):
    """Ensures that unicode prefixes raise a warning."""
    file_tokens = parse_tokens(mode(primitives_usages.format(primitive)))

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [UnicodeStringViolation])
    assert_error_text(visitor, primitive)


@pytest.mark.parametrize('primitive', [
    '"name"',
    'r"text"',
    "b'unicode'",
    '"u"',
    '"12"',
    'b""',
])
def test_correct_strings(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    primitive,
    mode,
):
    """Ensures that correct strings are fine."""
    file_tokens = parse_tokens(mode(primitives_usages.format(primitive)))

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
