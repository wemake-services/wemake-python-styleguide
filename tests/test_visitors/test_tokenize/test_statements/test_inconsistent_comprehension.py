import pytest

from wemake_python_styleguide.violations.consistency import (
    InconsistentComprehensionViolation,
)
from wemake_python_styleguide.visitors.tokenize.statements import (
    InconsistentComprehensionVisitor,
)

# Tests that should NOT be flagged

# List comprehension tests

correct_list_empty = """
a = []
"""

correct_list_one_line_comprehension = """
[some(number) for number in numbers]
"""

correct_list_other_one_line_comprehension = """
[
    some(number) for number in numbers
]
"""

correct_list_well_spaced_comprehension = """
[
    some(number)
    for number in matrix
    if number > 0
]
"""

correct_list_nested_comprehension = """
def get_all_args(call: ast.Call) -> Sequence[ast.AST]:
    return [
              *call.args,
              *[kw.value for kw in call.keywords],
    ]
"""


correct_list_ternary_in = """
[
    some(number) if letter in number else other(number)
    for number in matrix
    if number > 0
]
"""

correct_list_final_conditional_in = """
[
    some(number)
    for number in matrix
    if number in letters
]
"""


# Dictionary comprehension tests

correct_dict_empty = """
a = {{}}
"""

correct_dict_full = """
a = {'a':1,'b':2,'c':3}
"""

correct_dict_one_line_comprehension = """
{key:val for (key, val) in tuples}
"""

correct_dict_other_one_line_comprehension = """
{
    key:val for (key, val) in tuples
}
"""

correct_dict_well_spaced_comprehension = """
{
    key:val
    for (key, val) in matrix
    if key > 0
}
"""


# Set comprehensions

correct_set_empty = """
{{}}
"""

correct_set_one_line_comprehension = """
{some(number) for number in numbers}
"""

correct_set_other_one_line_comprehension = """
{
    some(number) for number in numbers
}
"""

correct_set_well_spaced_comprehension = """
{
    some(number)
    for number in matrix
    if number > 0
}
"""

# The below test is inspired by:
# https://python-reference.readthedocs.io/en/
#       latest/docs/comprehensions/set_comprehension.html
correct_set_nested_comprehension = """
{s for s in [1, 2, 3, 4]}
"""


# Generator comprehensions

correct_gen_empty = """
{{}}
"""

correct_gen_one_line_comprehension = """
(some(number) for number in numbers)
"""

correct_gen_other_one_line_comprehension = """
(
    some(number) for number in numbers
)
"""

correct_gen_well_spaced_comprehension = """
(
    some(number)
    for number in matrix
    if number > 0
)
"""


@pytest.mark.parametrize('code', [
    correct_list_empty,
    correct_list_one_line_comprehension,
    correct_list_other_one_line_comprehension,
    correct_list_well_spaced_comprehension,
    correct_list_nested_comprehension,
    correct_list_ternary_in,
    correct_list_final_conditional_in,
    correct_dict_empty,
    correct_dict_full,
    correct_dict_one_line_comprehension,
    correct_dict_other_one_line_comprehension,
    correct_dict_well_spaced_comprehension,
    correct_set_empty,
    correct_set_one_line_comprehension,
    correct_set_other_one_line_comprehension,
    correct_set_well_spaced_comprehension,
    correct_set_nested_comprehension,
    correct_gen_empty,
    correct_gen_one_line_comprehension,
    correct_gen_other_one_line_comprehension,
    correct_gen_well_spaced_comprehension,
])
def test_correct_comprehension(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct consistency does not raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = InconsistentComprehensionVisitor(default_options, file_tokens)
    visitor.run()

    assert_errors(visitor, [])


# Should raise flag

# List comprehension tests

wrong_list_almost_one_line = """
[
    some(number) for number in numbers
    if number > 0
]
"""

wrong_list_two_fors = """
[
    some(number)
    for numbers in matrix for number in numbers
]
"""

wrong_list_for_and_if = """
[
    some(number)
    for number in matrix if number > 0
]
"""

wrong_list_split_for_in = """
[
    some(number) for number
    in matrix
]
"""

# Dictionary comprehension tests

wrong_dict_almost_one_line = """
{
    key: val for (key, val) in tuples
    if key > 0
}
"""

wrong_dict_not_one_line_no_paren = """
{
    key: val for key, val in tuples
    if key > 0
}
"""

wrong_dict_two_lines_in_one = """
{
    key:val
    for numbers in matrix
    for (key, val) in numbers if key > 0
}
"""

wrong_dict_for_and_if = """
{
    some(number):other(number)
    for number in matrix if number > 0
}
"""


# Set comprehensions

wrong_set_almost_one_line = """
{
    some(number) for number in numbers
    if number > 0
}
"""

wrong_set_two_fors = """
{
    some(number)
    for numbers in matrix for number in numbers
}
"""

wrong_set_for_and_if = """
{
    some(number)
    for number in matrix if number > 0
}
"""


# Generator comprehensions

wrong_gen_almost_one_line = """
(
    some(number) for number in numbers
    if number > 0
)
"""

wrong_gen_two_fors = """
(
    some(number)
    for numbers in matrix for number in numbers
)
"""

wrong_gen_for_and_if = """
(
    some(number)
    for number in matrix if number > 0
)
"""


@pytest.mark.parametrize('code', [
    wrong_list_almost_one_line,
    wrong_list_two_fors,
    wrong_list_for_and_if,
    wrong_list_split_for_in,
    wrong_dict_almost_one_line,
    wrong_dict_not_one_line_no_paren,
    wrong_dict_two_lines_in_one,
    wrong_dict_for_and_if,
    wrong_set_almost_one_line,
    wrong_set_two_fors,
    wrong_set_for_and_if,
    wrong_gen_almost_one_line,
    wrong_gen_two_fors,
    wrong_gen_for_and_if,
])
def test_wrong_comprehension_consistency(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that wrong comprehension consistencies raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = InconsistentComprehensionVisitor(default_options, file_tokens)
    visitor.run()

    assert_errors(visitor, [InconsistentComprehensionViolation])
