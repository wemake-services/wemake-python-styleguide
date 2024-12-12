import pytest

from wemake_python_styleguide.violations.consistency import (
    UnderscoredNumberViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongNumberTokenVisitor,
)


@pytest.mark.parametrize('primitive', [
    '1_00',
    '10_00',
    '100_00',
    '-1_0',
    '-10_0',
    '-100_0',
    '1000_000',
    '-1000_000',
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
    """Ensures that wrongly underscored numbers raise a warning."""
    file_tokens = parse_tokens(mode(primitives_usages.format(primitive)))

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [UnderscoredNumberViolation])
    assert_error_text(visitor, primitive.lstrip('-').lstrip('+'))


@pytest.mark.parametrize('primitive', [
    '1000',
    '1000.0',
    '-333555',
    '-333555.5',
    '1_000',
    '1_000.0',
    '+1_000',
    '+1_000.0',
    '-1_000',
    '-1_000.0',
    '10_000',
    '100_000',
    '100_000_000',
    '"1_00"',
    '"10_00"',
    '"100_00"',
    '"-100_00"',
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

    visitor = WrongNumberTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])
