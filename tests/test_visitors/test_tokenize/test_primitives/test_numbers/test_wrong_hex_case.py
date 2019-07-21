# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    BadNumberSuffixViolation,
    WrongHexNumberCaseViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongNumberTokenVisitor,
)

hex_number_templates = [
    '0x{0}',
    '0xA{0}',
    '0x{0}D',
    '0x1{0}',
    '0x{0}1',
    '0xA{0}C',
    '0x1{0}2',
    '0x1{0}C',
    '0x{0}C1',
    '0x{0}CC',
    '0x11{0}',
]


@pytest.mark.parametrize('hex_char', ['a', 'b', 'c', 'd', 'e', 'f'])
@pytest.mark.parametrize('number', hex_number_templates)
def test_hex_wrong_case(
    parse_tokens,
    assert_errors,
    assert_error_text,
    default_options,
    hex_char,
    number,
    number_sign,
):
    """Ensures that numbers with suffix not in lowercase raise a warning."""
    real_number = number.format(hex_char)
    file_tokens = parse_tokens(number_sign(real_number))

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [WrongHexNumberCaseViolation])
    assert_error_text(visitor, real_number)


@pytest.mark.parametrize('hex_char', ['A', 'B', 'C', 'D', 'E', 'F'])
@pytest.mark.parametrize('number', hex_number_templates)
def test_hex_correct_case(
    parse_tokens,
    assert_errors,
    default_options,
    hex_char,
    number,
    number_sign,
):
    """Ensures that numbers with correct numbers do not raise a warning."""
    file_tokens = parse_tokens(number_sign(number.format(hex_char)))

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('hex_char', ['a', 'b', 'c', 'd', 'e', 'f'])
@pytest.mark.parametrize('number', hex_number_templates)
def test_hex_double_wrong_case(
    parse_tokens,
    assert_errors,
    assert_error_text,
    default_options,
    hex_char,
    number,
    number_sign,
):
    """Ensures that numbers with suffix not in lowercase raise a warning."""
    real_number = number.format(hex_char).replace('x', 'X')
    file_tokens = parse_tokens(number_sign(real_number))

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [
        BadNumberSuffixViolation,
        WrongHexNumberCaseViolation,
    ])
