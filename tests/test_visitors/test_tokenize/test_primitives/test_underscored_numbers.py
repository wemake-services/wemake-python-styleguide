# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    UnderscoredNumberViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongPrimitivesVisitor,
)


@pytest.mark.parametrize('primitive', [
    '10_00',
    '333_555',
    '3_3.3',
    '1_000_000',
    '-5_000',
    '-1_000.0',
])
def test_underscored_number(
    parse_tokens,
    assert_errors,
    assert_error_text,
    default_options,
    primitives_usages,
    primitive,
    mode,
):
    """Ensures that underscored numbers raise a warning."""
    file_tokens = parse_tokens(mode(primitives_usages.format(primitive)))

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [UnderscoredNumberViolation])
    assert_error_text(visitor, primitive.replace('-', ''))


@pytest.mark.parametrize('primitive', [
    '1000',
    '1000.0',
    '-333555',
    '-333555.5'
    '"10_00"',
])
def test_correct_number(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    primitive,
    mode,
):
    """Ensures that correct numbers are fine."""
    file_tokens = parse_tokens(mode(primitives_usages.format(primitive)))

    visitor = WrongPrimitivesVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
