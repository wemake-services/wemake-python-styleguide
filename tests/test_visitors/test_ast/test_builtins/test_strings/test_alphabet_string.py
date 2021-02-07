import string

import pytest

from wemake_python_styleguide.violations.best_practices import (
    StringConstantRedefinedViolation,
)
from wemake_python_styleguide.violations.consistency import (
    FormattedStringViolation,
)
from wemake_python_styleguide.visitors.ast.builtins import WrongStringVisitor


@pytest.mark.parametrize('code', [
    # We don't test all values here, because of strange parsing issues.
    string.digits,
    string.hexdigits,
    string.octdigits,

    string.ascii_uppercase,
    string.ascii_lowercase,
    string.ascii_letters,
])
@pytest.mark.parametrize('prefix', [
    '',
    'b',
    'u',
    'r',
    'rb',
])
def test_alphabet_as_string_violation(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    code,
    prefix,
    default_options,
):
    """Testing that the strings violate the rules."""
    tree = parse_ast_tree('{0}"{1}"'.format(prefix, code))

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [StringConstantRedefinedViolation])
    assert_error_text(visitor, code)


def test_alphabet_as_fstring_violation(
    assert_errors,
    parse_ast_tree,
    default_options,
):
    """Testing that the fstrings violate the rules."""
    tree = parse_ast_tree('f"{0}"'.format(string.ascii_letters))

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(
        visitor,
        [StringConstantRedefinedViolation],
        ignored_types=FormattedStringViolation,
    )


@pytest.mark.parametrize('code', [
    'ABCDE',
    '1234',
    'random text',
    r'\n',
    '!@#',
    '',
])
def test_alphabet_as_string_no_violation(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Testing that regular strings work well."""
    tree = parse_ast_tree('"{0}"'.format(code))

    visitor = WrongStringVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
