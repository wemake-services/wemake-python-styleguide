import pytest

from wemake_python_styleguide.violations.consistency import (
    MissingSpaceBetweenKeywordAndParenViolation,
)
from wemake_python_styleguide.visitors.tokenize.syntax import (
    WrongKeywordTokenVisitor,
)

multiline_error_function = """
def foo():
    yield(1, 2, 3)
"""

multiline_error_statement = """
assert(
    1, 2, 3,
) in b,
"""

multiline_correct_function = """
def foo():
    yield (1, 2, 3)
"""

multiline_correct_statement = """
assert (
    1, 2, 3,
) in b,
"""


@pytest.mark.parametrize('code', [
    'del(a)',
    'for(a, b) in [(1, 2)]:',
    'for (a, b) in((1, 2)):',
    'if a in(1, 2, 3):',
    'return(a)',
    'await(a)',
    'with(lambda x: x)() as (a, b)',
    'with (lambda x: x)() as(a, b)',
    '(a, b) is(a, b)',
    'from foo import(bar, baz, spam)',
    'except(ValueError, KeyError)',
    'elif(bar, baz)',
    'else(bar, baz)',
    multiline_error_function,
    multiline_error_statement,
])
def test_missing_space(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that parens right after keyword raise a warning."""
    file_tokens = parse_tokens(code, do_compile=False)

    visitor = WrongKeywordTokenVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [MissingSpaceBetweenKeywordAndParenViolation])


@pytest.mark.parametrize('code', [
    'del (a, b)',
    'for (a, b) in (1, 2, 3)',
    'return (a)',
    'await (a)',
    'with do_things() as (a, b)',
    '(a, b) is (a, b)',
    'from foo import (bar, baz, spam)',
    'except (ValueError, KeyError)',
    'elif (bar, baz)',
    'else (bar, baz)',
    multiline_correct_function,
    multiline_correct_statement,
])
def test_space_between_keyword_and_parens(
    parse_tokens,
    assert_errors,
    default_options,
    code,
):
    """Ensures that there's no violation if space in between."""
    file_tokens = parse_tokens(code, do_compile=False)

    visitor = WrongKeywordTokenVisitor(
        default_options, file_tokens=file_tokens,
    )
    visitor.run()

    assert_errors(visitor, [])
