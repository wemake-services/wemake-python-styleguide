import pytest

from wemake_python_styleguide.violations.consistency import (
    UnderscoredNumberViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongNumberTokenVisitor,
)


@pytest.mark.parametrize(
    'primitive',
    [
        '1_00',
        '10_00',
        '100_00',
        '-1_0',
        '-10_0',
        '-100_0',
        '1000_000',
        '-1000_000',
        '1.0_0',
        '3_3.3',
        '1_0_0',
        '1_0_0_1',
        '1_0_0.1',
        '0_0.00_1',
        '0.000_1',
        '0.00_01',
        '100_000.000_01',
        '100_00.000_001',
        '1000_000.000_001',
        '10_000_000.000000001',
        '10000000.000_000_001',
        '0b1_01',
        '0o10_11',
        '0x10_2',
        '1_234.157_001e-1123',
        '1_234.1_57001e-1_123',
        '12_34.157_001e-1123',
        '1e1_1',
        '1_1e1',
        '3_3j',
        '0.5_6j',
    ],
)
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


@pytest.mark.parametrize(
    'primitive',
    [
        '-333555',
        '-333555.5',
        '+1_000',
        '+1_000.0',
        '-1_000',
        '-1_000.0',
        '10_000',
        '100_000',
        '100_000_000',
        '0.0_005',
        '10_000_000.000_000_001',
        '10_000_000.0_001',
        '10_000_000.001',
        '10_000_000.01',
        '10_000_000.1',
        '0b1_001',
        '0o10_101',
        '0x100_234',
        '1_234.157_001e-1_123',
        '3_333j',
        '3j',
        '0.5_655j',
        '0.555j',
    ],
)
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


def test_numbers_do_not_error(
    parse_tokens,
    default_options,
    primitives_usages,
    mode,
):  # pragma: no cover
    """Ensures that correct numbers are fine."""
    try:
        from test.test_grammar import VALID_UNDERSCORE_LITERALS  # noqa: PLC0415
    except Exception:
        pytest.skip('VALID_UNDERSCORE_LITERALS did not import')
    for number in VALID_UNDERSCORE_LITERALS:
        file_tokens = parse_tokens(mode(primitives_usages.format(number)))

        visitor = WrongNumberTokenVisitor(
            default_options, file_tokens=file_tokens
        )
        visitor.run()
