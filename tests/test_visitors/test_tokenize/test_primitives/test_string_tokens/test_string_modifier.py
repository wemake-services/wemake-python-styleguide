# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    UppercaseStringModifierViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    RawStringNotNeededViolation,
    WrongStringTokenVisitor,
)

@pytest.mark.parametrize('modifier', [
    'b',
    'f',
    '',  # special case, no modifier is used
])
@pytest.mark.parametrize('primitive', [
    '{0}""',
    "{0}''",
    '{0}"Big text"',
    "{0}'Format 123'",
])
def test_correct_prefix(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    primitive,
    modifier,
    mode,
):
    """Ensures that correct prefixes work."""
    string = primitive.format(modifier)
    file_tokens = parse_tokens(mode(primitives_usages.format(string)))

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('modifier', [
    'r',
    'rb',
    'fr',
])
@pytest.mark.parametrize('primitive', [
    '{0}"\\"',
    "{0}'\\'",
    '{0}"Big \\text"',
    "{0}'Format \\123'",
])
def test_correct_prefix_raw_string(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    primitive,
    modifier,
    mode,
):
    """Ensures that correct prefixes work."""
    string = primitive.format(modifier)
    file_tokens = parse_tokens(mode(primitives_usages.format(string)))

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])

@pytest.mark.parametrize('modifier', [
    'B',
    'F',
])
@pytest.mark.parametrize('primitive', [
    '{0}""',
    "{0}''",
    '{0}"Big text"',
    "{0}'Format 123'",
])
def test_uppercase_prefix(
    parse_tokens,
    assert_errors,
    assert_error_text,
    default_options,
    primitives_usages,
    primitive,
    modifier,
    mode,
):
    """Ensures that uppercase modifiers are restricted."""
    string = primitive.format(modifier)
    file_tokens = parse_tokens(mode(primitives_usages.format(string)))

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [UppercaseStringModifierViolation])
    assert_error_text(visitor, modifier)


@pytest.mark.parametrize('modifier', [
    'RF',
    'FR',
    'RB',
    'BR',
])
@pytest.mark.parametrize('primitive', [
    '{0}""',
    "{0}''",
    '{0}"text"',
    "{0}'123'",
])
def test_uppercase_prefix_multiple(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    primitive,
    modifier,
    mode,
):
    """Ensures that uppercase modifiers are restricted."""
    string = primitive.format(modifier)
    file_tokens = parse_tokens(mode(primitives_usages.format(string)))

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [
        UppercaseStringModifierViolation,
        UppercaseStringModifierViolation,
        RawStringNotNeededViolation,
    ])
