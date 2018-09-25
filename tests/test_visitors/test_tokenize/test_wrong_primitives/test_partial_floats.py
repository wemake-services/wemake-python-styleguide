# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.visitors.tokenize.wrong_primitives import (
    PartialFloatViolation,
    WrongPrimitivesVisitor,
)


@pytest.mark.parametrize('code', [
    'x = 10.',
    'print(3. + 5.1)',
    '.05 + 1.2',
])
def test_partial_float(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that partial floats raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [PartialFloatViolation])


@pytest.mark.parametrize('code', [
    'x = 10.0',
    'print(3.0 + 5.1)',
    '0.05 + 1.2',
])
def test_correct_float(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct floats are fine."""
    file_tokens = parse_tokens(code)

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
