import pytest

from wemake_python_styleguide.violations.consistency import (
    LineCompriseCarriageReturnViolation,
)
from wemake_python_styleguide.visitors.tokenize.syntax import (
    WrongKeywordTokenVisitor,
)

# Correct:

correct_newline = 'print(1)\nprint(2)'
correct_nl = 'print(1,\n    2)'
correct_string = '"\r"'
correct_raw_string = 'r"\r"'
correct_real_newline = """
print(1)
print(2)
"""

# Wrong:

wrong_newline_single = 'print(1)\r\nprint(2)'
wrong_newline_sequenced1 = 'print(1)\nprint(2)\r\n'
wrong_newline_sequenced2 = 'print(1)\r\nprint(2)\n'
wrong_newline_sequenced3 = 'print(1,\r\n    2)'
wrong_newline_in_multiline = """print(2)\r
print(3)
"""


@pytest.mark.parametrize('code', [
    wrong_newline_single,
    wrong_newline_sequenced1,
    wrong_newline_sequenced2,
    wrong_newline_sequenced3,
    wrong_newline_in_multiline,
])
def test_string_wrong_line_breaks(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that obsolete string's line break raise a violation."""
    file_tokens = parse_tokens(code)

    visitor = WrongKeywordTokenVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [LineCompriseCarriageReturnViolation])


@pytest.mark.parametrize('code', [
    correct_newline,
    correct_nl,
    correct_string,
    correct_raw_string,
    correct_real_newline,
])
def test_string_proper_line_breaks(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that proper string's line break are fine."""
    file_tokens = parse_tokens(code, do_compile=False)

    visitor = WrongKeywordTokenVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])
