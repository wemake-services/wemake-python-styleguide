import pytest

from wemake_python_styleguide.violations.consistency import (
    InconsistentComprehensionViolation,
)
from wemake_python_styleguide.visitors.tokenize.statements import (
    InconsistentComprehensionVisitor,
)

# Tests that should NOT be flagged

# List comprehension tests

correct_empty_list = """
a = []
"""

correct_full_list = """
a = [1,2,3]
"""

correct_one_line_comprehension = """
[some(number) for number in numbers]
"""

correct_well_spaced_comprehension = """
[
    some(number)
    for number in matrix
    if number > 0
]
"""


@pytest.mark.parametrize('code', [
    correct_empty_list,
    correct_full_list,
    correct_one_line_comprehension,
    correct_well_spaced_comprehension,
])
def test_correct_comprehension_consistency(
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

wrong_because_almost_one_line = """
[
    some(number) for number in numbers
    if number > 0
]
"""

wrong_because_two_lines_in_one = """
[
    some(number)
    for numbers in matrix
    for number in numbers if number > 0
]
"""


@pytest.mark.parametrize('code', [
    wrong_because_almost_one_line,
    wrong_because_two_lines_in_one,
])
def test_wrong_comprehension_use(
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
