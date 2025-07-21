import pytest

from wemake_python_styleguide.compat.constants import PY312
from wemake_python_styleguide.violations.best_practices import (
    CommentInFormattedStringViolation,
)
from wemake_python_styleguide.visitors.tokenize.comments import (
    CommentInFormattedStringVisitor,
)

if not PY312:  # pragma: >=3.12 no cover
    pytest.skip(
        reason='comments in fstring was added in 3.12',
        allow_module_level=True,
    )

# Correct
fstring_without_comments = """
foo = f"test{a}"
"""

fstring_with_hash_single_quotes = """
foo = f'test {a} # testing'
"""

fstring_with_hash = """
foo = f"test{a} # testing"
"""

fstring_with_hash_between_braces = """
foo = f"test{a} # comment {b} # comment"
"""


fstring_with_two_values = """
f"My name is {name} and I am {age} years old."
"""


fstring_with_math_operation = """
f"The sum of {x} and {y} is {x + y}."
"""

fstring_with_hash_between_quotes = """
foo = f"hello" # comment "{bar}" # comment"
"""


fstring_in_docstring = '''
foo = f"""hello"{bar}" # comment world"""
'''

# Wrong
fstring_with_comment = """
foo = f"test{a # comment
}"
"""

rfstring_with_comment = """
foo = rf"test{a # comment
}"
"""

rfstring_with_comment_single_quotes = """
foo = rf'test{a # comment
}'
"""


rfstring_with_comment_triple_quotes = '''
foo = rf"""test{a # comment
}"""
'''

rfstring_with_comment_triple_single_quotes = """
foo = rf'''test{a # comment
}'''
"""


frstring_with_comment = """
foo = fr"test{a # comment
}"
"""

frstring_with_comment_single_quotes = """
foo = fr'test{a # comment
}'
"""


frstring_with_comment_triple_quotes = '''
foo = fr"""test{a # comment
}"""
'''

frstring_with_comment_triple_single_quotes = """
foo = fr'''test{a # comment
}'''
"""

fstring_with_comment_single_quotes = """
foo = f'test{a # comment
}'
"""

fstring_with_comment_and_hash_on_new_line = """
foo = f"test{a # comment
} # comment"
"""

fstring_with_two_values_and_comment = """
foo = f"test{a} and test{b # Testing values
}"
"""


multiline_fstring_with_comment = """
foo = (f"test{value}"
       f"test{another_value}"
       f"test{wrong # This is not allowed
       }"
       f"test{value}")
"""

fstring_with_comment_and_second_line = """
foo = f"hello{bar # comment
}world"
"""

fstring_with_comment_between_quotes = """
foo = f"hello'{bar # comment
}'world"
"""

fstring_with_comment_in_docstring = '''
foo = f"""hello"{bar # comment
}world"""
'''


@pytest.mark.parametrize(
    'code',
    [
        fstring_without_comments,
        fstring_with_hash_single_quotes,
        fstring_with_two_values,
        fstring_with_math_operation,
        fstring_with_hash,
        fstring_with_hash_between_braces,
        fstring_in_docstring,
        fstring_with_hash_between_quotes,
    ],
)
def test_correct_formatted_string(
    parse_tokens,
    assert_errors,
    default_options,
    code,
) -> None:
    """Check that there are no violations in the correct string."""
    file_tokens = parse_tokens(code)

    visitor = CommentInFormattedStringVisitor(
        default_options,
        file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'code',
    [
        fstring_with_comment,
        fstring_with_comment_single_quotes,
        fstring_with_comment_and_second_line,
        fstring_with_two_values_and_comment,
        multiline_fstring_with_comment,
        fstring_with_comment_and_hash_on_new_line,
        fstring_with_comment_between_quotes,
        fstring_with_comment_in_docstring,
        rfstring_with_comment,
        rfstring_with_comment_triple_quotes,
        rfstring_with_comment_single_quotes,
        rfstring_with_comment_triple_single_quotes,
        frstring_with_comment,
        frstring_with_comment_triple_quotes,
        frstring_with_comment_single_quotes,
        frstring_with_comment_triple_single_quotes,
    ],
)
def test_wrong_formatted_string(
    parse_tokens,
    assert_errors,
    default_options,
    code,
) -> None:
    """Checking that the wrong string has violations."""
    file_tokens = parse_tokens(code)

    visitor = CommentInFormattedStringVisitor(
        default_options,
        file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [CommentInFormattedStringViolation])
