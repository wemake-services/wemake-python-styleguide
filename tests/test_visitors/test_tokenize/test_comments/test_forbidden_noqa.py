import pytest

from wemake_python_styleguide.violations.best_practices import (
    ForbiddenInlineIgnoreViolation,
)
from wemake_python_styleguide.visitors.tokenize.comments import NoqaVisitor


@pytest.mark.parametrize(('code', 'forbidden_inline_ignore'), [
    ('x = 10_00  # noqa: WPS002,Z114', ('A', 'C', 'WPS002')),
    ('x = 10_00  # noqa:W002, U114', ('W',)),
    ('x = 10_00  # noqa: J002, WPS114', ('J', 'WPS')),
    ('x = 10_00  # noqa: J, WPS114', ('J',)),
    ('x = 10_00  # noqa: WPS114', ('WPS',)),
])
def test_forbidden_noqa(
    parse_tokens,
    assert_errors,
    options,
    code,
    forbidden_inline_ignore,
):
    """Ensure that noqa comments with forbidden violations raise a violation."""
    file_tokens = parse_tokens(code)
    options = options(forbidden_inline_ignore=forbidden_inline_ignore)
    visitor = NoqaVisitor(options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [ForbiddenInlineIgnoreViolation])


@pytest.mark.parametrize(('code', 'forbidden_inline_ignore'), [
    ('x = 10_00  # noqa: WPS002,Z114', ('W',)),
    ('x = 10_00  # noqa: WPS002,Z114', ('Z1',)),
])
def test_correct_noqa(
    parse_tokens,
    assert_errors,
    options,
    code,
    forbidden_inline_ignore,
):
    """Ensure that proper noqa comments do not rise violations."""
    file_tokens = parse_tokens(code)
    options = options(forbidden_inline_ignore=forbidden_inline_ignore)
    visitor = NoqaVisitor(options, file_tokens=file_tokens)
    visitor.run()
    assert_errors(visitor, [])
