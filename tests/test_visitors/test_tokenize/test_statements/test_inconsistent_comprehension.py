import pytest

from wemake_python_styleguide.violations.consistency import (
    InconsistentComprehensionViolation,
)
from wemake_python_styleguide.visitors.tokenize.statements import (
    InconsistentComprehensionVisitor,
)

# Tests that should NOT be flagged

# List comprehension tests

correct_list_empty = '[]'

correct_list_one_line_comprehension1 = """
def wrapper():
    [some(number) for number in numbers]
"""

correct_list_one_line_comprehension2 = """
def wrapper():
    [a + b for a in a_ for b in b_]
"""

correct_list_one_line_comprehension3 = """
def wrapper():
    [a + b for a in a_ for b in b_ if a]
"""

correct_list_one_line_comprehension4 = """
def wrapper():
    [a + b for a in a_ for b in b_ if a if b]
"""

correct_list_other_one_line_comprehension = """
def wrapper():
    [
        some(number) for number in numbers
    ]
"""

correct_list_well_spaced_comprehension = """
def wrapper():
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


correct_list_ternary1 = """
def wrapper():
    all_unused = all(
        is_local if access.is_protected(vn) else access.is_unused(vn)
        for vn in all_names
    )
"""


correct_list_ternary2 = """
def wrapper():
    [
        some(number) if letter in number else other(number)
        for number in matrix
        if number > 0
    ]
"""

correct_list_final_conditional_in = """
def wrapper():
    [
        some(number)
        for number in matrix
        if number in letters
    ]
"""

correct_list_two_compehensions1 = """
def wrapper():
    comp = [
        [a + 1 for a in b]
        for b in some
        if b > 0
    ]
"""

correct_list_two_compehensions2 = """
def wrapper():
    comp = [
        [
            a + 1
            for a in b
        ]
        for b in some
        if b > 0
    ]
"""


# Dictionary comprehension tests

correct_dict_empty = '{{}}'

correct_dict_full = """
a = {'a':1,'b':2,'c':3}
"""

correct_dict_one_line_comprehension = """
def wrapper():
    {key:val for (key, val) in tuples}
"""

correct_dict_other_one_line_comprehension = """
def wrapper():
    {
        key:val for (key, val) in tuples
    }
"""

correct_dict_well_spaced_comprehension = """
def wrapper():
    {
        key:val
        for (key, val) in matrix
        if key > 0
    }
"""


# Set comprehensions

correct_set = '{1, 2, 3}'

correct_set_one_line_comprehension = """
def wrapper():
    {some(number) for number in numbers}
"""

correct_set_other_one_line_comprehension = """
def wrapper():
    {
        some(number) for number in numbers
    }
"""

correct_set_well_spaced_comprehension = """
def wrapper():
    {
        some(number)
        for number in matrix
        if number > 0
    }
"""

correct_set_complex_comprehension = """
def wrapper():
    {
        some(number)
        for number in matrix
        for other in iterable
        if number > 0
        if other > 0
    }
"""

# The below test is inspired by:
# https://python-reference.readthedocs.io/en/
#       latest/docs/comprehensions/set_comprehension.html
correct_set_nested_comprehension1 = """
def wrapper():
    {s for s in [1, 2, 3, 4]}
"""

correct_set_nested_comprehension2 = """
def wrapper():
    {s for s in {1, 2, 3, 4}}
"""

correct_set_nested_comprehension3 = """
def wrapper():
    {s for s in (1, 2, 3, 4)}
"""


# Generator comprehensions

correct_gen_one_line_comprehension = """
def wrapper():
    (some(number) for number in numbers)
"""

correct_gen_ternary_in_comprehension1 = """
def wrapper():
    (some(number) for number in (other if other else some))
"""

correct_gen_ternary_in_comprehension2 = """
def wrapper():
    (some(number) for number in (other if other else some) if number)
"""

correct_gen_ternary_in_comprehension3 = """
def wrapper():
    (
        some(number)
        for number in (other if other else some)
    )
"""

correct_gen_ternary_in_comprehension4 = """
def wrapper():
    (
        some(number)
        for number in (other if other else some)
        if number
    )
"""

correct_gen_ternary_in_comprehension5 = """
def wrapper():
    (
        some(number * x)
        for number in (other if other else some)
        for x in matrix
        if number
    )
"""

correct_gen_ternary_in_comprehension6 = """
def wrapper():
    (
        some(number * x)
        for x in matrix
        for number in (other if other else some)
    )
"""

correct_gen_other_one_line_comprehension = """
def wrapper():
    (
        some(number) for number in numbers
    )
"""

correct_gen_well_spaced_comprehension = """
def wrapper():
    (
        some(number)
        for number in matrix
        if number > 0
    )
"""


@pytest.mark.parametrize('code', [
    correct_list_empty,
    correct_list_one_line_comprehension1,
    correct_list_one_line_comprehension2,
    correct_list_one_line_comprehension3,
    correct_list_one_line_comprehension4,
    correct_list_other_one_line_comprehension,
    correct_list_well_spaced_comprehension,
    correct_list_nested_comprehension,
    correct_list_ternary1,
    correct_list_ternary2,
    correct_list_final_conditional_in,
    correct_list_two_compehensions1,
    correct_list_two_compehensions2,
    correct_dict_empty,
    correct_dict_full,
    correct_dict_one_line_comprehension,
    correct_dict_other_one_line_comprehension,
    correct_dict_well_spaced_comprehension,
    correct_set,
    correct_set_one_line_comprehension,
    correct_set_other_one_line_comprehension,
    correct_set_well_spaced_comprehension,
    correct_set_nested_comprehension1,
    correct_set_nested_comprehension2,
    correct_set_nested_comprehension3,
    correct_set_complex_comprehension,
    correct_gen_one_line_comprehension,
    correct_gen_ternary_in_comprehension1,
    correct_gen_ternary_in_comprehension2,
    correct_gen_ternary_in_comprehension3,
    correct_gen_ternary_in_comprehension4,
    correct_gen_ternary_in_comprehension5,
    correct_gen_ternary_in_comprehension6,
    correct_gen_other_one_line_comprehension,
    correct_gen_well_spaced_comprehension,
])
def test_correct_comprehension(
    parse_tokens,
    assert_errors,
    default_options,
    code,
    mode,
):
    """Ensures that correct consistency does not raise a warning."""
    file_tokens = parse_tokens(mode(code))

    visitor = InconsistentComprehensionVisitor(default_options, file_tokens)
    visitor.run()

    assert_errors(visitor, [])


# Should raise flag

# List comprehension tests

wrong_list_almost_one_line = """
def wrapper():
    [
        some(number) for number in numbers
        if number > 0
    ]
"""

wrong_list_two_fors = """
def wrapper():
    [
        some(number)
        for numbers in matrix for number in numbers
    ]
"""

wrong_list_for_and_if = """
def wrapper():
    [
        some(number)
        for number in matrix if number > 0
    ]
"""

wrong_list_split_for_in = """
def wrapper():
    [
        some(number) for number
        in matrix
    ]
"""

wrong_list_split_multiple_ifs1 = """
def wrapper():
    [
        some(number)
        for number in matrix if some
        if number > 0
    ]
"""

wrong_list_split_multiple_ifs2 = """
def wrapper():
    [
        some(number)
        for number in matrix if some if number > 0
    ]
"""

wrong_list_two_compehensions1 = """
def wrapper():
    comp = [
        [a + 1 for a in b]
        for b in some if b > 0
    ]
"""

wrong_list_two_compehensions2 = """
def wrapper():
    comp = [
        [
            a + 1 for a in b
            if a > 0
        ]
        for b in some
        if b > 0
    ]
"""

# Dictionary comprehension tests

wrong_dict_almost_one_line = """
def wrapper():
    {
        key: val for (key, val) in tuples
        if key > 0
    }
"""

wrong_dict_not_one_line_no_paren = """
def wrapper():
    {
        key: val for key, val in tuples
        if key > 0
    }
"""

wrong_dict_two_lines_in_one = """
def wrapper():
    {
        key:val
        for numbers in matrix
        for (key, val) in numbers if key > 0
    }
"""

wrong_dict_for_and_if = """
def wrapper():
    {
        some(number):other(number)
        for number in matrix if number > 0
    }
"""


# Set comprehensions

wrong_set_almost_one_line = """
def wrapper():
    {
        some(number) for number in numbers
        if number > 0
    }
"""

wrong_set_two_fors = """
def wrapper():
    {
        some(number)
        for numbers in matrix for number in numbers
    }
"""

wrong_set_for_and_if = """
def wrapper():
    {
        some(number)
        for number in matrix if number > 0
    }
"""


# Generator comprehensions

wrong_gen_almost_one_line = """
def wrapper():
    (
        some(number) for number in numbers
        if number > 0
    )
"""

wrong_gen_two_fors = """
def wrapper():
    (
        some(number)
        for numbers in matrix for number in numbers
    )
"""

wrong_gen_for_and_if = """
def wrapper():
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
    wrong_list_split_multiple_ifs1,
    wrong_list_split_multiple_ifs2,
    wrong_list_two_compehensions1,
    wrong_list_two_compehensions2,
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
    mode,
):
    """Ensures that wrong comprehension consistencies raise a warning."""
    file_tokens = parse_tokens(mode(code))

    visitor = InconsistentComprehensionVisitor(default_options, file_tokens)
    visitor.run()

    assert_errors(visitor, [InconsistentComprehensionViolation])


# async keyword placement

wrong_async_set = """
async def wrapper():
    {
        some(elem) async
        for elem in other
        for other in iterable
    }
"""

wrong_async_dict = """
async def wrapper():
    {
        some(elem): 0 async
        for elem in other
        if elem
    }
"""

wrong_async_list1 = """
async def wrapper():
    [
        some(elem)
        for other in iterable async
        for elem in other
    ]
"""

wrong_async_list2 = """
async def wrapper():
    [
        some(elem) async
        for other in iterable
        for elem in other
    ]
"""

wrong_async_gen1 = """
async def wrapper():
    (
        some(elem) async
        for elem in other
    )
"""

wrong_async_gen2 = """
async def wrapper():
    (
        some(elem) async
        # comment
        for elem in other
    )
"""


@pytest.mark.parametrize('code', [
    wrong_async_set,
    wrong_async_dict,
    wrong_async_list1,
    wrong_async_list2,
    wrong_async_gen1,
    wrong_async_gen2,
])
def test_wrong_async_keyword_placement(
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
