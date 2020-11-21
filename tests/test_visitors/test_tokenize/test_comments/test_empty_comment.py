import pytest

from wemake_python_styleguide.violations.best_practices import (
    EmptyCommentViolation
)
from wemake_python_styleguide.visitors.tokenize.comments import (
    WrongCommentVisitor
)


# TODO:
# Replace the violation and visitor later after we implement them

# add test for inline comment

# Be aware of code coverage
# what about alerting in the right line? since we only alert the first line of a block


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

# empty_line = ""
# empty_comment = "#"


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

non_empty_comment = "# Non empty text"
code_statement = "my_var = 1"

@pytest.mark.parametrize('pattern', [
    single_empty_wrapped,
    multi_empty_wrapped
])
@pytest.mark.parametrize('comment', [
    non_empty_comment
])
def test_correct_doc_comment(
    parse_tokens,
    assert_errors,
    default_options,
    pattern,
    comment,
):
    """Ensures that correct comments do not raise a warning."""
    file_tokens = parse_tokens(pattern.format(comment))

    print(pattern.format(comment))

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    # print(visitor)
    assert(False)

    assert_errors(visitor, [])


@pytest.mark.parametrize('pattern', [
    single_empty_beginning,
    single_empty_end,
    multi_empty_beginning,
    multi_empty_end

])
@pytest.mark.parametrize('code_or_comment', [
    non_empty_comment,
    code_statement
])
def test_incorrect_doc_comment(
    parse_tokens,
    assert_errors,
    default_options,
    pattern,
    code_or_comment,
):
    """Ensures that incorrect empty comments raise a warning."""
    file_tokens = parse_tokens(pattern.format(code_or_comment))

    print(pattern.format(code_or_comment))

    visitor = WrongCommentVisitor(default_options, file_tokens=file_tokens)
    visitor.run()
    # print(visitor)
    assert(False)

    assert_errors(visitor, [EmptyCommentViolation])
