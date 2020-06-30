import pytest

from wemake_python_styleguide.violations.consistency import FloatZeroViolation
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongNumberTokenVisitor,
)


def test_float_zero(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    mode,
):
    """Ensures that float zeros (0.0) raise a warning."""
    primitive = 0.0  # noqa: WPS358
    file_tokens = parse_tokens(mode(primitives_usages.format(primitive)))

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [FloatZeroViolation])


@pytest.mark.parametrize('primitive', [
    '0',
    'float(0)',
    '5',
    '30.4',
])
def test_correct_zero_and_non_zero_numbers(
    parse_tokens,
    assert_errors,
    default_options,
    primitives_usages,
    primitive,
    mode,
):
    """Ensures that correct zeros and non-zero numbers don't raise a warning."""
    file_tokens = parse_tokens(mode(primitives_usages.format(primitive)))

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
