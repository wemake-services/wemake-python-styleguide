import pytest

from wemake_python_styleguide.violations.consistency import (
    BracketBlankLineViolation,
)
from wemake_python_styleguide.visitors.tokenize.statements import (
    BracketLocationVisitor,
)

# Correct:

correct_empty_module = ''
correct_single_line = 'arr = []'
correct_single_line_items = 'arr = [1, 2, 3]'
correct_single_line_call = 'some(1, 2, 3)'

correct_method = """
class Some(object):
    '''
    Dco.

    Some [
        Example,
    ]
    '''

    def __init__(self, node=None, text: Optional[str] = None) -> None:
        ...
"""

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
    # comment
    1,

    2,
]
"""

correct_comment_in_middle_of_list = """
arr = [
    1,

    # comment
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

wrong_blank_line_after_comment = """
extra_new_line = [  # some

    'wrong',
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
    2,
)
"""

wrong_blank_line_at_end_parens = """
arr = (
    1, 2,

)
"""


@pytest.mark.parametrize('code', [
    correct_empty_module,
    correct_single_line,
    correct_single_line_call,
    correct_single_line_items,
    correct_method,
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

    visitor = BracketLocationVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_blank_line_at_start_list,
    wrong_blank_line_at_end_list,
    wrong_blank_line_after_comment,
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

    visitor = BracketLocationVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [BracketBlankLineViolation])
