import pytest

from wemake_python_styleguide.violations.consistency import (
    ImplicitRawStringViolation,
    UnicodeStringViolation,
    UppercaseStringModifierViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongStringTokenVisitor,
)


@pytest.mark.parametrize('code', [
    r"'\\a'",
    r"'\\n'",
    r"'\\\\'",
    r"'some \\ escaped'",
    r"b'\\a'",
    r'"""\\1"""',
    r"'''\\ '''",
])
def test_implicit_raw_string(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that implicit raw strings raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [ImplicitRawStringViolation])


@pytest.mark.parametrize('code', [
    r"'\\'",
    r"r'\\'",
    r"'\n'",
    r"r'\n'",
    r"r'some \\ escaped'",
    r"r'some \n escaped'",
    r"br'\\a'",
    r'r"""\\text"""',
    r"r'''\\ '''",
])
def test_explicit_raw_string(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that implicit raw strings raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    r"u'\\4'",
    r"u'\\n'",
    r"u'\\\\'",
    r"u'some \\ escaped'",
])
def test_implicit_unicode_raw_string(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that implicit unicode raw string raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [
        UnicodeStringViolation,
        ImplicitRawStringViolation,
    ])


@pytest.mark.parametrize('code', [
    r"U'\\4'",
    r"U'\\n'",
    r"U'\\\\'",
    r"U'some \\ escaped'",
])
def test_implicit_upercase_unicode_raw_string(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that implicit uppercase unicode raw string raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = WrongStringTokenVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [
        UnicodeStringViolation,
        UppercaseStringModifierViolation,
        ImplicitRawStringViolation,
    ])
