# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    NumberWithMeaninglessZeroViolation
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongNumberTokenVisitor
)


@pytest.mark.parametrize('number', [
    '0b0001',
    '0x001',
    '0o05',
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
    assert_error_text(visitor, number.replace('-', ''))


@pytest.mark.parametrize('number', [
    '0b1',
    '0x1',
    '0o5',
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


@pytest.mark.parametrize('code', [
    'print("0b1")',
    'print("0x1")',
    'print("0o5")',
])
@pytest.mark.parametrize('number', [
    '0b1',
    '0x1',
    '0o5',
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
