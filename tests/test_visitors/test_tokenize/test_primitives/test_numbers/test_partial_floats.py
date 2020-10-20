import pytest

from wemake_python_styleguide.violations.consistency import (
    NumberWithMeaninglessZeroViolation,
    PartialFloatViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongNumberTokenVisitor,
)


@pytest.mark.parametrize('primitive', [
    '10.',
    '.05',
    '.0',
    '0.',
    '-5.',
    '-.43',
])
def test_partial_float(
    parse_tokens,
    assert_errors,
    assert_error_text,
    default_options,
    primitives_usages,
    primitive,
    mode,
):
    """Ensures that partial floats raise a warning."""
    file_tokens = parse_tokens(mode(primitives_usages.format(primitive)))

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [PartialFloatViolation])
    assert_error_text(visitor, primitive.replace('-', ''))


@pytest.mark.parametrize('primitive', [
    '10.0',
    '0.14',
    '-0.05',
    '-1.1',
])
def test_correct_float(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    primitive,
    mode,
):
    """Ensures that correct floats are fine."""
    file_tokens = parse_tokens(mode(primitives_usages.format(primitive)))

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('primitive', [
    '.0500',
    '.00',
])
def test_double_incorrect_float(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    primitive,
    number_sign,
    mode,
):
    """Ensures that partial floats raise a warning."""
    file_tokens = parse_tokens(
        mode(primitives_usages.format(number_sign(primitive))),
    )

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [
        PartialFloatViolation,
        NumberWithMeaninglessZeroViolation,
    ])
