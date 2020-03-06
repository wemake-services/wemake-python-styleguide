import pytest

from wemake_python_styleguide.violations.consistency import (
    WrongBracketPositionViolation,
)
from wemake_python_styleguide.visitors.tokenize.statements import (
    BracketLocationVisitor,
)

# Correct:

correct_simple_variable = 'xy = [[], [], ()]'
correct_simple_function_call = 'print([1, 2, 3], (1, 2))'
correct_annotated_variable = 'xy: Optional[int] = some()'

correct_function = """
def first(arg: int) -> int:
    ...
"""

correct_multiline_function = """
def first(
    arg: int
) -> Tuple[int, int]:
    ...
"""

correct_multiline_call = """
print([
    0,
    [1],
    (2, 2),
    {3, 3, 3},
])
"""

correct_multiline_list = """
some = [[
    1, 2, 3,
]]
"""

correct_multiline_tuple = """
some = (
    [1, 1, 1],
    2,
    {3, 3},
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

correct_enclosure_call = """
ClassName(
    1, 2, 3,
)()
"""

# Wrong:

wrong_multiline_function = """
def second(
    args: Tuple[int, int]) -> None: ...
"""

wrong_multiline_call = """
print(
    1, 2, 3)
"""

wrong_multiline_tuple = """
some = (
    [1, 1, 1],
    2,
    3)
"""

wrong_multiline_dict1 = """
some = {
        1: [
            1,
            1,
            1],
        2: 2,
        3: 3,
}
"""

wrong_multiline_dict2 = """
some = {
        1: [
            1,
            1,
            1,
        ],
        2: 2,
        3: 3}
"""

wrong_multiline_list = """
some = [
    1,
    2,
    3]
"""


@pytest.mark.parametrize('code', [
    correct_simple_variable,
    correct_simple_function_call,
    correct_annotated_variable,
    correct_function,
    correct_multiline_function,
    correct_multiline_call,
    correct_multiline_list,
    correct_multiline_tuple,
    correct_multiline_dict,
    correct_multiline_call,
    correct_enclosure_call,
])
def test_correct_bracket(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that correct brackets works."""
    file_tokens = parse_tokens(code)

    visitor = BracketLocationVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('code', [
    wrong_multiline_function,
    wrong_multiline_call,
    wrong_multiline_tuple,
    wrong_multiline_dict1,
    wrong_multiline_dict2,
    wrong_multiline_list,
])
def test_wrong_brackets(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that incorrect brackets raise a warning."""
    file_tokens = parse_tokens(code)

    visitor = BracketLocationVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [WrongBracketPositionViolation])
