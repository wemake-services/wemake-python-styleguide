# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    UnderscoredNumberViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongPrimitivesVisitor,
)


@pytest.mark.parametrize('code', [
    'x = 10_00',
    'print(333_555)',
    '3_3 + 55',
])
def test_underscored_number(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that underscored numbers raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [UnderscoredNumberViolation])


@pytest.mark.parametrize('code', [
    'x = 1000',
    'print(333555)',
    '33 + 55',
    '_ = 12',
    'print("10_00")',
])
def test_correct_number(
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
