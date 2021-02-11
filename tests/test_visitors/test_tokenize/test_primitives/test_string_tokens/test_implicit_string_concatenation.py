import pytest

from wemake_python_styleguide.violations.consistency import (
    ImplicitStringConcatenationViolation,
)
from wemake_python_styleguide.visitors.tokenize.primitives import (
    WrongStringConcatenationVisitor,
)

# Correct:

correct_string_sum = 'some = "a" + "b"'

correct_tuple_with_strings = """
some = ('a', 'b', "c")
"""

correct_tuple_with_strings_nextline = """
some = (
    'a', 'b', "c",
)
"""

correct_tuple_with_strings_multiline = """
some = (
    "a",
    "b",
    "c",
)
"""

# Wrong:

wrong_inline_string_concatenation = """
some = ('a' 'b')
"""

wrong_inline_string_concatenation_nextline = """
some = (
    "a" 'b',
)
"""

wrong_inline_string_concatenation_multiline = """
some = (
    'a'
    b'b'
)
"""

wrong_inline_string_concatenation_w_comment = """
some = (
    'a'  # Comment
    'b'
)
"""


@pytest.mark.parametrize('code', [
    wrong_inline_string_concatenation,
    wrong_inline_string_concatenation_nextline,
    wrong_inline_string_concatenation_multiline,
    wrong_inline_string_concatenation_w_comment,
])
def test_implicit_string_concatenation(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that implicit string concatenation raise a warning."""
    file_tokens = parse_tokens(code, do_compile=False)

    visitor = WrongStringConcatenationVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [ImplicitStringConcatenationViolation])


@pytest.mark.parametrize('code', [
    correct_string_sum,
    correct_tuple_with_strings,
    correct_tuple_with_strings_nextline,
    correct_tuple_with_strings_multiline,
])
def test_correct_strings(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct strings are fine."""
    file_tokens = parse_tokens(code)

    visitor = WrongStringConcatenationVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])
