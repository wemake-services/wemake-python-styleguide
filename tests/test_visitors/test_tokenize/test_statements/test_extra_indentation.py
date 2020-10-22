import pytest

from wemake_python_styleguide.violations.consistency import (
    ExtraIndentationViolation,
)
from wemake_python_styleguide.visitors.tokenize.statements import (
    ExtraIndentationVisitor,
)

# Correct:

correct_function_with_docstring = """
def first():
    '''Some text'''
    return None
"""

correct_multiple_functions = """
def first():
    if some:
        return 1
    return 2

def second(args: Tuple[int, int]) -> None:
    print(
        args[0],
        args[1],
    )
"""

correct_multiline_tuple = """
some = (
    [1, 1, 1],
    2,
    3,
)
"""

correct_multiline_dict = """
some = {
    1: [
        1,
        1,
        1,
    ],
    2: 2,
    3: 3,
}
"""

correct_multiline_call = """
print(
    'a',
    object(),
    [2, 3],
)
"""

# Wrong:

wrong_function_with_docstring = """
def first():
        '''Some text'''
        return None
"""

wrong_multiple_functions = """
def first():
    if some:
            return 1
    return 2

def second(args: Tuple[int, int]) -> None:
    print(
        args[0],
        args[1],
    )
"""

wrong_multiline_tuple = """
some = (
        [1, 1, 1],
        2,
        3,
)
"""

wrong_multiline_dict = """
some = {
        1: [
            1,
            1,
            1,
        ],
        2: 2,
        3: 3,
}
"""

wrong_multiline_call = """
print(
            'a',
            object(),
            [2, 3],
)
"""

wrong_single_paren = """
some_set = {1
           }
"""


@pytest.mark.parametrize('code', [
    correct_function_with_docstring,
    correct_multiple_functions,
    correct_multiline_tuple,
    correct_multiline_dict,
    correct_multiline_call,
])
def test_correct_indentation(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct indentation works."""
    file_tokens = parse_tokens(code)

    visitor = ExtraIndentationVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_function_with_docstring,
    wrong_multiple_functions,
    wrong_multiline_tuple,
    wrong_multiline_dict,
    wrong_multiline_call,
    wrong_single_paren,
])
def test_wrong_indentation(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that incorrect indentation raises a warning."""
    file_tokens = parse_tokens(code)

    visitor = ExtraIndentationVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [ExtraIndentationViolation])
