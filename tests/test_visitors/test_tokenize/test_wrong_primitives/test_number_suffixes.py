# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    BadNumberSuffixViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongPrimitivesVisitor,
)


@pytest.mark.parametrize('code', [
    'x = 0XFF',
    'print(1.5E+10)',
    '0O11 + 5',
    'y = 0B1001',
])
def test_bad_number_suffixes(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that numbers with suffix not in lowercase raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [BadNumberSuffixViolation])


@pytest.mark.parametrize('code', [
    'x = 0xFF',
    'print(1.5e+10)',
    '0o11 + 5',
    'y = 0b1001',
    'print("0XFF")',
    'regular = "XOBE"',
])
def test_correct_number_suffixes(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct numbers are fine."""
    file_tokens = parse_tokens(code)

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
