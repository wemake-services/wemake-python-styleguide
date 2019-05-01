# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    NumberWithMeaninglessZeroViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongNumberTokenVisitor,
)


@pytest.mark.parametrize('number', [
    '0b00001',
    '0x001',
    '0o001',
    '1e01',
])
def test_bad_number_meaningless_zero(
    parse_tokens,
    assert_errors,
    assert_error_text,
    default_options,
    primitives_usages,
    number,
    mode,
):
    """Ensures that numbers with meaningless zero raise a warning."""
    file_tokens = parse_tokens(mode(primitives_usages.format(number)))
    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [NumberWithMeaninglessZeroViolation])


@pytest.mark.parametrize('number', [
    '0b1',
    '0b1',
    '0x1',
    '0o1',
    '123e1',
])
def test_correct_number_meaningless_zero(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    number,
    mode,
):
    """Ensures that correct numbers are fine."""
    file_tokens = parse_tokens(mode(primitives_usages.format(number)))
    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [])


@pytest.mark.parametrize('number', [
    '0b01',
    '0x01',
    '0o01',
    '0b0110',
    '0x0110',
    '0o0110',
    '0b0001',
])
def test_correct_number_with2n_digits(
    parse_tokens,
    assert_errors,
    assert_error_text,
    default_options,
    primitives_usages,
    number,
    mode,
):
    """Ensures that numbers with 2n digits and meaningless zero are fine."""
    file_tokens = parse_tokens(mode(primitives_usages.format(number)))
    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    'print("{0}")',
    "print('{0}')",
])
@pytest.mark.parametrize('number', [
    '0b1',
    '0x1',
    '0o5',
    '1e1',
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
    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [])
