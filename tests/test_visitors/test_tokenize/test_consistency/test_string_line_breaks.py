# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    LineCompriseCarriageReturnViolation,
)
from wemake_python_styleguide.visitors.tokenize.syntax import (
    WrongKeywordTokenVisitor,
)

# Correct:

correct_string_line_break = 'string with line break \n sequence is OK'

# Wrong:

wrong_string_line_break_single = 'string with \r (carriage return) line break is wrong'

wrong_string_line_break_sequence = 'string contains \r\n sequence is wrong'

wrong_string_line_break_multiline = """
string with carriage return line break \r in
some multiple line is improper too
"""


@pytest.mark.parametrize('code', [
    wrong_string_line_break_single,
    wrong_string_line_break_sequence,
    wrong_string_line_break_multiline,
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
    correct_string_line_break,
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
