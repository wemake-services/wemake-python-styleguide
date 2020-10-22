import pytest

from wemake_python_styleguide.violations.consistency import (
    BadNumberSuffixViolation,
    NumberWithMeaninglessZeroViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongNumberTokenVisitor,
)


@pytest.mark.parametrize('number', [
    '0.10',
    '21.5400',

    '0x00A',

    '0e01',
    '1.5e010',
    '1.5e-010',

    '0o00007',

    '0b0001',
])
def test_meaningless_zeros(
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

    assert_errors(visitor, [NumberWithMeaninglessZeroViolation])
    assert_error_text(visitor, number.lstrip('-').lstrip('+'))


@pytest.mark.parametrize('number', [
    '0X0A',
    '0E09',
    '0B01',
    '0O07',
])
def test_meaningless_zeros_and_case(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    number,
    number_sign,
    mode,
):
    """Ensures that numbers raise two violations."""
    file_tokens = parse_tokens(
        mode(primitives_usages.format(number_sign(number))),
    )

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [
        BadNumberSuffixViolation,
        NumberWithMeaninglessZeroViolation,
    ])


@pytest.mark.parametrize('number', [
    '1234567890',

    '20.05',

    '0x0',
    '0xA00',

    '0e0',
    '1.5e10',
    '1.5e-100',

    '0o0',
    '0o10',

    '0b0',
    '0b100000',
])
def test_correct_zeros(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    number,
    number_sign,
    mode,
):
    """Ensures that correct numbers are fine."""
    file_tokens = parse_tokens(
        mode(primitives_usages.format(number_sign(number))),
    )

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
