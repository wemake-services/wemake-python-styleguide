from textwrap import indent

import pytest

from wemake_python_styleguide.violations.naming import (
    UnusedVariableIsDefinedViolation,
)
from wemake_python_styleguide.visitors.ast.naming import (
    WrongVariableUsageVisitor,
)

module_context = '{0}'

function_context = """
def function():
{0}
"""

method_context = """
class Test(object):
    def function():
    {0}
"""


@pytest.mark.parametrize(('context', 'indentation'), [
    (function_context, 4),
    (method_context, 8),
])
@pytest.mark.parametrize('bad_name', [
    '_unused',
    '_',
    '__',
])
def test_unused_variable_definition(
    assert_errors,
    parse_ast_tree,
    context,
    indentation,
    bad_name,
    forbidden_unused_template,
    default_options,
):
    """Testing that any variable cannot be used if it is marked as unused."""
    tree = parse_ast_tree(
        context.format(
            indent(
                forbidden_unused_template.format(bad_name),
                ' ' * indentation,
            ),
        ),
    )

    visitor = WrongVariableUsageVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnusedVariableIsDefinedViolation])


@pytest.mark.parametrize(('context', 'indentation'), [
    (function_context, 4),
    (method_context, 8),
])
@pytest.mark.parametrize('bad_name', [
    '(_first, _second)',
])
def test_unused_variable_tuple_definition(
    assert_errors,
    parse_ast_tree,
    context,
    indentation,
    bad_name,
    forbidden_tuple_unused_template,
    default_options,
):
    """Testing that any variable cannot be used if it is marked as unused."""
    tree = parse_ast_tree(
        context.format(
            indent(
                forbidden_tuple_unused_template.format(bad_name),
                ' ' * indentation,
            ),
        ),
    )

    visitor = WrongVariableUsageVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnusedVariableIsDefinedViolation])


@pytest.mark.parametrize(('context', 'indentation'), [
    (module_context, 0),
    (function_context, 4),
    (method_context, 8),
])
@pytest.mark.parametrize('bad_name', [
    '(first, second)',
    '(first, _second)',
    '(_first, second)',
])
def test_used_variable_tuple_definition(
    assert_errors,
    parse_ast_tree,
    context,
    indentation,
    bad_name,
    forbidden_tuple_unused_template,
    default_options,
):
    """Testing that any variable can be used if it is marked as unused."""
    tree = parse_ast_tree(
        context.format(
            indent(
                forbidden_tuple_unused_template.format(bad_name),
                ' ' * indentation,
            ),
        ),
    )

    visitor = WrongVariableUsageVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(('context', 'indentation'), [
    (module_context, 0),
    (function_context, 4),
    (method_context, 8),
])
@pytest.mark.parametrize('bad_name', [
    '_protected',
    '_unused',
])
def test_unused_variable_definition_allowed(
    assert_errors,
    parse_ast_tree,
    context,
    indentation,
    bad_name,
    allowed_unused_template,
    default_options,
):
    """Testing that any variable can be used in some cases."""
    tree = parse_ast_tree(
        context.format(
            indent(
                allowed_unused_template.format(bad_name),
                ' ' * indentation,
            ),
        ),
    )

    visitor = WrongVariableUsageVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])


@pytest.mark.parametrize(('context', 'indentation'), [
    (module_context, 0),
    (function_context, 4),
    (method_context, 8),
])
@pytest.mark.parametrize('bad_name', [
    '_',
    '__',
])
def test_raw_unused_variable_definition(
    assert_errors,
    parse_ast_tree,
    context,
    indentation,
    bad_name,
    forbidden_raw_unused_template,
    default_options,
):
    """Testing that any variable can be used in some cases."""
    tree = parse_ast_tree(
        context.format(
            indent(
                forbidden_raw_unused_template.format(bad_name),
                ' ' * indentation,
            ),
        ),
    )

    visitor = WrongVariableUsageVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [UnusedVariableIsDefinedViolation])


@pytest.mark.parametrize(('context', 'indentation'), [
    (module_context, 0),
    (function_context, 4),
    (method_context, 8),
])
@pytest.mark.parametrize('bad_name', [
    'regular',
    'list_',
])
def test_used_variable_definition(
    assert_errors,
    parse_ast_tree,
    context,
    indentation,
    bad_name,
    naming_template,
    default_options,
):
    """Testing that any variable cannot be used if it is marked as unused."""
    tree = parse_ast_tree(
        context.format(
            indent(
                naming_template.format(bad_name), ' ' * indentation,
            ),
        ),
    )

    visitor = WrongVariableUsageVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
