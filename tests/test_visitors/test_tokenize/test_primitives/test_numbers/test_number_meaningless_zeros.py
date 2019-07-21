# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    NumberWithMeaninglessZeroViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongNumberTokenVisitor,
)


@pytest.mark.parametrize('number', [
    '0x01',
    '0x00A',

    '0e00',
    '0e01',
    '1.5e+010',
    '1.5e-010',

    '0o01',
    '0o00007',

    '0b0001',
    '0b01',

    '-0x01',
    '-0x00A',

    '-0e00',
    '-0e01',
    '-1.5e-010',

    '-0o01',
    '-0o00007',

    '-0b0001',
    '-0b01',

    '+0x01',
    '+0x00A',

    '+0e00',
    '+0e01',
    '+1.5e+010',
    '+1.5e-010',

    '-0o01',
    '-0o00007',

    '-0b0001',
    '-0b01',
    '--0b0001',
    '++0b01',
    '-+0b0001',
])
def test_meaningless_zeros(
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

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [NumberWithMeaninglessZeroViolation])
    assert_error_text(visitor, number.lstrip('-').lstrip('+'))


@pytest.mark.parametrize('number', [
    '0x0',
    '0x10',
    '0xA00',

    '0e0',
    '0e10',
    '1.5e+10',
    '1.5e-100',

    '0o0',
    '0o1',
    '0o7000',

    '0b0',
    '0b1',
    '0b100000',

    '-0x0',
    '-0x10',
    '-0xA00',

    '-0e0',
    '-0e10',
    '-1.5e+10',
    '-1.5e-100',

    '-0o0',
    '-0o1',
    '0o7000',

    '-0b0',
    '-0b1',
    '-0b100000',

    '+0x0',
    '+0x10',
    '+0xA00',

    '+0e0',
    '+0e10',
    '+1.5e+10',
    '+1.5e-100',

    '+0o0',
    '+0o1',
    '+0o7000',

    '+0b0',
    '+0b1',
    '+0b100000',
])
def test_correct_zeros(
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
    'as_string = "{0}"',
])
@pytest.mark.parametrize('number', [
    '0x0FF',
    '1.5e+01',
    '0o011',
    '0b01001',

    '-0x0FF',
    '-1.5e+01',
    '-0o011',
    '-0b01001',

    '+0x0FF',
    '+1.5e+01',
    '+0o011',
    '+0b01001',
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
