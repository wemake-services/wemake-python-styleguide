from contextlib import suppress

import pytest

from wemake_python_styleguide.constants import SPECIAL_ARGUMENT_NAMES_WHITELIST
from wemake_python_styleguide.violations.naming import (
    ReservedArgumentNameViolation,
)
from wemake_python_styleguide.visitors.ast.naming.validation import (
    WrongNameVisitor,
)

# Correct:

correct_method_template = """
class Test:
    def method({0}, different):
        ...
"""

correct_classmethod_template = """
class Test:
    @classmethod
    def method({0}, different):
        ...
"""

correct_function_template = 'def function({0}, different): ...'


@pytest.mark.parametrize('argument', SPECIAL_ARGUMENT_NAMES_WHITELIST)
def test_reserved_argument_name(
    assert_errors,
    assert_error_text,
    parse_ast_tree,
    default_options,
    naming_template,
    mode,
    argument,
):
    """Ensures that special names for arguments are restricted."""
    with suppress(SyntaxError):
        # We use `suppress` here because some fixtures
        # have duplicated `self` or `cls` arguments.
        tree = parse_ast_tree(mode(naming_template.format(argument)))

        visitor = WrongNameVisitor(default_options, tree=tree)
        visitor.run()

        assert_errors(visitor, [ReservedArgumentNameViolation])
        assert_error_text(visitor, argument)


@pytest.mark.parametrize('argument', SPECIAL_ARGUMENT_NAMES_WHITELIST)
@pytest.mark.parametrize(
    'code',
    [
        correct_method_template,
        correct_classmethod_template,
        correct_function_template,
    ],
)
def test_correct_argument_name(
    assert_errors,
    parse_ast_tree,
    default_options,
    code,
    mode,
    argument,
):
    """Ensures that special names for arguments are restricted."""
    tree = parse_ast_tree(mode(code.format(argument)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(
    'variable_name',
    ['_SELF', '_Self', 'Self', '_CLS', 'cLs', '_clS', '_MCS', 'mcS', '_mCs'],
)
def test_reserved_argument_name_variations(
    assert_errors,
    parse_ast_tree,
    default_options,
    simple_variables_template,
    mode,
    variable_name,
):
    """Ensures variations of special names are allowed for simple variables."""
    tree = parse_ast_tree(mode(simple_variables_template.format(variable_name)))

    visitor = WrongNameVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
