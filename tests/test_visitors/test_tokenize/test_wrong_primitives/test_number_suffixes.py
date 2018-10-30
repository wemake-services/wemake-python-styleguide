# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    BadNumberSuffixViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongPrimitivesVisitor,
)


@pytest.mark.parametrize('number', [
    '0XFF',
    '1.5E+10',
    '0O11',
    '0B1001',
    '-0XFF',
    '-1.5E+10',
    '-0O11',
    '-0B1001',
])
def test_bad_number_suffixes(
    parse_tokens,
    assert_errors,
    assert_error_text,
    default_options,
    primitives_usages,
    number,
    mode,
):
    """Ensures that numbers with suffix not in lowercase raise a warning."""
    file_tokens = parse_tokens(mode(primitives_usages.format(number)))

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [BadNumberSuffixViolation])
    assert_error_text(visitor, number.replace('-', ''))


@pytest.mark.parametrize('number', [
    '0xFF',
    '1.5e+10',
    '0o11',
    '0b1001',
    '-0xAF',
    '-3e+10',
    '-0o11',
    '-0b1111',
])
def test_correct_number_suffixes(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    number,
    mode,
):
    """Ensures that correct numbers are fine."""
    file_tokens = parse_tokens(mode(primitives_usages.format(number)))

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    'print("0XFF")',
    'regular = "XOBE"',
])
@pytest.mark.parametrize('number', [
    '0xFF',
    '1.5e+10',
    '0o11',
    '0b1001',
    '-0xAF',
    '-3e+10',
    '-0o11',
    '-0b1111',
])
def test_similar_strings(
    parse_tokens,
    assert_errors,
    default_options,
    code,
    number,
    mode,
):
    """Ensures that strings are fine."""
    file_tokens = parse_tokens(mode(code.format(number)))

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
