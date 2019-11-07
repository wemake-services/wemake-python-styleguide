# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.consistency import (
    UselessBlankLineViolation,
)
from wemake_python_styleguide.visitors.tokenize.statements import (
    BlankLineVisitor,
)

# Correct:

correct_blank_line_in_middle_list = """
arr = [
    1,

    2,
]
"""

correct_blank_line_in_middle_dict = """
arr = {
    1:

    2,
}
"""

correct_blank_line_in_middle_parens = """
arr = (
    1,

    2,
)
"""

correct_comment_start_of_list = """
arr = [
    #comment
    1,

    2,
]
"""

correct_comment_in_middle_of_list = """
arr = [
    1,

    #comment
    2,
]
"""

# Wrong:

wrong_blank_line_at_start_list = """
some = [

    1,
    2,
    3,
    ]
"""

wrong_blank_line_at_end_list = """
some = [
    1,
    2,
    3,

    ]
"""

wrong_blank_line_at_start_dict = """
arr = {

    1: 2,
}
"""

wrong_blank_line_at_end_dict = """
arr = {
    1: 2,

}
"""

wrong_blank_line_at_start_parens = """
arr = (

    1,
    2
)
"""

wrong_blank_line_at_end_parens = """
arr = (
    1, 2

)
"""


@pytest.mark.parametrize('code', [
    correct_blank_line_in_middle_list,
    correct_blank_line_in_middle_dict,
    correct_blank_line_in_middle_parens,
    correct_comment_start_of_list,
    correct_comment_in_middle_of_list,
])
def test_correct_blank_lines(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct blank lines work."""
    file_tokens = parse_tokens(code)

    visitor = BlankLineVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_blank_line_at_start_list,
    wrong_blank_line_at_end_list,
    wrong_blank_line_at_start_dict,
    wrong_blank_line_at_end_dict,
    wrong_blank_line_at_start_parens,
    wrong_blank_line_at_end_parens,
])
def test_wrong_blank_lines(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that incorrect blank lines raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = BlankLineVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [UselessBlankLineViolation])
