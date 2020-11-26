import pytest

from wemake_python_styleguide.violations.best_practices import (
    EmptyCommentViolation,
)
from wemake_python_styleguide.visitors.tokenize.comments import (
    WrongCommentVisitor,
)

inline_comment = """
four = 4
seven = 7  #
"""

end_of_file_comment = """
# Non-empty
#
#
# Next line will trigger violation
#
#
"""

max_one_alert_per_block = """
#
# Previous line will trigger violation
#
# Non-empty
#
#
"""

single_empty_wrapped = """
{0}
#
{0}
"""

multi_empty_wrapped = """
{0}
#
#
{0}
"""

single_empty_beginning = """
#
{0}
"""

single_empty_end = """
{0}
#
"""

multi_empty_beginning = """
#
#
{0}
"""

multi_empty_end = """
{0}
#
#
"""

non_empty_comment = '# Non empty text'
code_statement = 'my_var = 1'


@pytest.mark.parametrize('pattern', [
    single_empty_wrapped,
    multi_empty_wrapped,
])
@pytest.mark.parametrize('comment', [
    non_empty_comment,
])
def test_correct_empty_comment(
    parse_tokens,
    assert_errors,
    default_options,
    pattern,
    comment,
):
    """Ensures that correct comments do not raise a warning."""
    file_tokens = parse_tokens(pattern.format(comment))

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize('pattern', [
    single_empty_beginning,
    single_empty_end,
    multi_empty_beginning,
    multi_empty_end,
])
@pytest.mark.parametrize('code_or_comment', [
    non_empty_comment,
    code_statement,
])
def test_incorrect_empty_comment(
    parse_tokens,
    assert_errors,
    default_options,
    pattern,
    code_or_comment,
):
    """Ensures that incorrect empty comments raise a warning."""
    file_tokens = parse_tokens(pattern.format(code_or_comment))

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [EmptyCommentViolation])


@pytest.mark.parametrize('edge_case', [
    inline_comment,
    end_of_file_comment,
    max_one_alert_per_block,
])
def test_edge_case_empty_comment(
    parse_tokens,
    assert_errors,
    default_options,
    edge_case,
):
    """Ensures that edge cases incorrect empty comments raise a warning."""
    file_tokens = parse_tokens(edge_case)

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()

    assert_errors(visitor, [EmptyCommentViolation])
