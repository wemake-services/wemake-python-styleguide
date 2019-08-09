# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    BadComplexNumberSuffixViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongNumberTokenVisitor,
)


@pytest.mark.parametrize('number', [
    '1J',
    '2J + 10',
])
def test_bad_complex_suffix(
    parse_tokens,
    assert_errors,
    assert_error_text,
    default_options,
    primitives_usages,
    number,
    number_sign,
    mode,
):
    """Ensures that numbers with suffix not in lowercase raise a warning."""
    file_tokens = parse_tokens(
        mode(primitives_usages.format(number_sign(number))),
    )

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [BadComplexNumberSuffixViolation])
    assert_error_text(visitor, 'J')


@pytest.mark.parametrize('number', [
    '1j',
    '2j + 10',
])
def test_correct_complex_suffix(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    number,
    number_sign,
    mode,
):
    """Ensures that numbers with suffix not in lowercase raise a warning."""
    file_tokens = parse_tokens(
        mode(primitives_usages.format(number_sign(number))),
    )

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
