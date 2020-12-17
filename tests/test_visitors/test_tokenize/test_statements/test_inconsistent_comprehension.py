import pytest

from wemake_python_styleguide.violations.consistency import (
    InconsistentComprehensionViolation,
)
from wemake_python_styleguide.visitors.tokenize.statements import (
    InconsistentComprehensionVisitor,
)

just_a_list = '''
a = []
'''


@pytest.mark.parametrize('code', [
    just_a_list,
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


wrong_because_almost_one_line = '''
[
    some(number) for number in numbers
    if number > 0
]
'''


@pytest.mark.parametrize('code', [
    wrong_because_almost_one_line,
])
def test_wrong_multiline_string_use(
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
