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

correct_list_full = """
a = [1,2,3]
"""

correct_list_one_line_comprehension = """
[some(number) for number in numbers]
"""

correct_list_well_spaced_comprehension = """
[
    some(number)
    for number in matrix
    if number > 0
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

correct_dict_well_spaced_comprehension = """
{
    key:val
    for (key, val) in matrix
    if key > 0
}
"""


@pytest.mark.parametrize('code', [
    correct_list_empty,
    correct_list_full,
    correct_list_one_line_comprehension,
    correct_list_well_spaced_comprehension,
])
def test_correct_list_comprehension_consistency(
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


@pytest.mark.parametrize('code', [
    correct_dict_empty,
    correct_dict_full,
    correct_dict_one_line_comprehension,
    correct_dict_well_spaced_comprehension,
])
def test_correct_dict_comprehension_consistency(
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

wrong_list_because_almost_one_line = """
[
    some(number) for number in numbers
    if number > 0
]
"""

# Dictionary comprehension tests

wrong_dict_because_almost_one_line = """
{
    key:val for (key, val) in tuples
    if key > 0
}
"""


@pytest.mark.parametrize('code', [
    wrong_list_because_almost_one_line,
])
def test_wrong_multiline_string_use_list(
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


@pytest.mark.parametrize('code', [
    wrong_dict_because_almost_one_line,
])
def test_wrong_multiline_string_use_dict(
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
