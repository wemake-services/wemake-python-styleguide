# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    LineCompriseCarriageReturnViolation,
)
from wemake_python_styleguide.visitors.tokenize.syntax import (
    WrongKeywordTokenVisitor,
)

# Correct:

correct_newline = 'print(1)\nprint(2)'
correct_string_composed = 'some_string = "\r"'

# Wrong:

wrong_newline_single = 'print(1)\rprint(2)'
wrong_newline_sequenced = 'print(1)\r\nprint(2)'
wrong_newline_in_multiline = """print(1)\rprint(2)\r
print(3).
"""


@pytest.mark.parametrize('code', [
    wrong_newline_single,
    wrong_newline_sequenced,
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
    correct_string_composed,
])
def test_string_proper_line_breaks(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that proper string's line break are fine."""
    file_tokens = parse_tokens(code)

    visitor = WrongKeywordTokenVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])
