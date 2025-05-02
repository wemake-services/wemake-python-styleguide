import pytest

from wemake_python_styleguide.violations.best_practices import (
    CommentInFormattedStringViolation,
)
from wemake_python_styleguide.visitors.tokenize.comments import (
    CommentInFormattedStringVisitor,
)

# Correct
fstring_without_comments = """
foo = f"test{a}"
"""

fstring_with_hash = """
foo = f"test{a} # testing"
"""

fstring_with_two_values = """
f"My name is {name} and I am {age} years old."
"""


fstring_with_math_operation = """
f"The sum of {x} and {y} is {x + y}."
"""

# Wrong
fstring_with_comment = """
foo = f"test{a # comment
}"
"""

fstring_with_comment_and_second_line = """
foo = f"hello{bar # comment
}world"
"""


@pytest.mark.parametrize(
    'code',
    [
        fstring_without_comments,
        fstring_with_two_values,
        fstring_with_math_operation,
        fstring_with_hash,
    ],
)
def test_correct_formatted_string(
    parse_tokens, assert_errors, default_options, code
) -> None:
    """Check that there are no violations in the correct string."""
    file_tokens = parse_tokens(code)

    visitor = CommentInFormattedStringVisitor(
        default_options, file_tokens=file_tokens
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code', [fstring_with_comment, fstring_with_comment_and_second_line]
)
def test_wrong_formatted_string(
    parse_tokens, assert_errors, default_options, code
) -> None:
    """Checking that the wrong string has violations."""
    file_tokens = parse_tokens(code)

    visitor = CommentInFormattedStringVisitor(
        default_options, file_tokens=file_tokens
    )
    visitor.run()

    assert_errors(visitor, [CommentInFormattedStringViolation])
