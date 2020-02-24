# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    RawStringNotNeededViolation,
    UppercaseStringModifierViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongStringTokenVisitor,
)


@pytest.mark.parametrize('modifier', [
    'r',
    'rb',
    'fr',
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

    assert_errors(
        visitor,
        [],
        ignored_types=(RawStringNotNeededViolation,),
    )


@pytest.mark.parametrize('modifier', [
    'R',
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

    assert_errors(
        visitor,
        [UppercaseStringModifierViolation],
        ignored_types=(RawStringNotNeededViolation,),
    )
    assert_error_text(visitor, modifier, multiple=True)


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


@pytest.mark.parametrize('raw_strings', [
    "{0}'Carriage return \r'",
    "{0}'Escaped \' quote'",
    "{0}'Escaped ab \t'",
    "{0}'Escaped backslash \\'",
])
def test_necessary_raw_string(
    parse_tokens,
    assert_errors,
    default_options,
    raw_strings,
):
    """Ensures that correct usage of raw string works."""
    string = raw_strings.format('r')
    file_tokens = parse_tokens(string)

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('raw_strings', [
    "{0}'No escaped caracter'",
    '{0}"Here neither"',
    "{0}'''Not here as well'''",
])
def test_unnecessary_raw_string(
    parse_tokens,
    assert_errors,
    default_options,
    raw_strings,
):
    """Ensures that usage of raw string is forbidden if no backslash."""
    string = raw_strings.format('r')
    file_tokens = parse_tokens(string)

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [RawStringNotNeededViolation])
