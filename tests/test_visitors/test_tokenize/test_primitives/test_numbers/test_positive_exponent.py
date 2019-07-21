# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    BadNumberSuffixViolation,
    NumberWithMeaninglessZeroViolation,
    PositiveExponentViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongNumberTokenVisitor,
)


@pytest.mark.parametrize('number', [
    '1.5e+10',
    '1e+1',
    '0e+0',
    '10e+10',

    '-1.5e+10',
    '-1e+1',
    '-0e+0',
    '-10e+10',

    '+1.5e+10',
    '+1e+1',
    '+0e+0',
    '+10e+10',
])
def test_positive_exponent(
    parse_tokens,
    assert_errors,
    assert_error_text,
    default_options,
    primitives_usages,
    number,
    mode,
):
    """Ensures that numbers with positive exponent are incorrect."""
    file_tokens = parse_tokens(mode(primitives_usages.format(number)))

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [PositiveExponentViolation])
    assert_error_text(visitor, number.lstrip('-').lstrip('+'))


@pytest.mark.parametrize('number', [
    '-1',
    '1234567890',
    '0xE',
    '0xEE',

    '1.5e10',
    '1e1',
    '0e0',
    '10e10',

    '1.5e-10',
    '1e-1',
    '0e-0',
    '10e-10',

    '-1.5e10',
    '-1e1',
    '-0e0',
    '-10e10',

    '+1.5e10',
    '+1e1',
    '+0e0',
    '+10e10',

    '-1.5e-10',
    '-1e-1',
    '-0e-0',
    '-10e-10',

    '+1.5e-10',
    '+1e-1',
    '+0e-0',
    '+10e-10',
])
def test_correct_exponent(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    number,
    mode,
):
    """Ensures that correct exponent is allowed."""
    file_tokens = parse_tokens(mode(primitives_usages.format(number)))

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('number', [
    '1.5E+01',
    '-10.5E+01',
    '+1E+01',
])
def test_all_error_in_exponent(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    number,
    mode,
):
    """Ensures that numbers with positive exponent are incorrect."""
    file_tokens = parse_tokens(mode(primitives_usages.format(number)))

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [
        BadNumberSuffixViolation,
        NumberWithMeaninglessZeroViolation,
        PositiveExponentViolation,
    ])
